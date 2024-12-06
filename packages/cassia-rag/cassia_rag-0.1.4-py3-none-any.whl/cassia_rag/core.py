from owlready2 import *
import json
from datetime import datetime
import pandas as pd
import os
import pandas as pd
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document


def get_tissue_markers(file_path, tissue_name, species_name=None):
    """
    Extract markers for a specific tissue and species from the marker database.
    If species not found, defaults to human data.
    
    Args:
        file_path (str): Path to the marker database CSV file
        tissue_name (str): Name of the tissue to filter for
        species_name (str, optional): Name of the species to filter for. If not found, will use human data.
    
    Returns:
        pd.DataFrame: Processed marker data
    """
    # Try different encodings
    encodings_to_try = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    
    def read_csv_with_encoding(file_path, encodings):
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                print(f"Successfully read file with {encoding} encoding")
                return df
            except UnicodeDecodeError:
                continue
        raise ValueError("Could not read file with any of the specified encodings")

    try:
        df = read_csv_with_encoding(file_path, encodings_to_try)
    except ValueError as e:
        print(f"Error: {e}")
        return None

    # Convert tissue and species columns to lowercase
    df['Tissue_lower'] = df['Tissue'].str.lower()
    df['Species_lower'] = df['Species'].str.lower()
    
    # Filter for tissue
    df_filtered = df[df['Tissue_lower'] == tissue_name.lower()]
    
    if len(df_filtered) == 0:
        print(f"No data found for tissue: {tissue_name}")
        return None
    
    # Filter for species if specified
    if species_name:
        species_filtered = df_filtered[df_filtered['Species_lower'] == species_name.lower()]
        
        # If no data for specified species, use human data
        if len(species_filtered) == 0:
            print(f"No data found for species: {species_name}. Using human data instead.")
            human_filtered = df_filtered[df_filtered['Species_lower'] == 'human']
            
            if len(human_filtered) == 0:
                print("No human data found either. Using all species data.")
            else:
                df_filtered = human_filtered
        else:
            print(f"Found data for species: {species_name}")
            df_filtered = species_filtered

    # Create directory
    output_dir = f"./{tissue_name}_{species_name}"
    os.makedirs(output_dir, exist_ok=True)

    # Transform the data
    transformed_df = (df_filtered
        [['Cell_Ontology_ID', 'Cell_Name', 'Symbol', 'Species']]
        .groupby('Cell_Name')
        .agg({
            'Cell_Ontology_ID': 'first',
            'Symbol': lambda x: ', '.join(sorted(set(x))),
            'Species': lambda x: ', '.join(sorted(set(x)))
        })
        .reset_index()
    )

    transformed_df = transformed_df.rename(columns={'Symbol': 'Markers'})

    # Create output filename
    filename = f"{tissue_name.lower()}"
    if species_name:
        filename += f"_{species_name.lower()}"
    filename += "_celltypes_markers.csv"
    
    output_file = os.path.join(output_dir, filename)
    transformed_df.to_csv(output_file, index=False, encoding='utf-8')

    print(f"\nResults saved to: {output_file}")
    return transformed_df

# Example usage:
#result_df = get_tissue_markers("~/Canonical_Marker (1).csv", "Lung", "Fetal")

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
import pandas as pd
import os

def analyze_tissue_markers(csv_path, tissue_type, target_species, model_choice='claude'):
    """
    Analyze tissue markers for annotation with reference to other species' data.
    
    Args:
        csv_path (str): Path to the markers CSV file generated in previous step
        tissue_type (str): Type of tissue to analyze
        target_species (str): Species being annotated
        model_choice (str): Choice of language model ('gpt' or 'claude')
    """
    
    # Read the markers CSV
    df = pd.read_csv(csv_path)
    reference_species = ', '.join(df['Species'].unique())
    markers_text = df.to_string()

    # Custom text splitter for marker data
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n", ","]
    )
    
    # Convert DataFrame to documents for RAG
    docs = [Document(page_content=markers_text)]
    splits = text_splitter.split_documents(docs)
    
    # Create vector store
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

    # Create the prompt template
    MARKER_ANALYSIS_PROMPT = f"""
    You are an expert in biology specializing in {tissue_type} annotation. 
    You are analyzing {target_species} {tissue_type} data, with reference markers and cell types from {reference_species}.

    Given the following cell type and marker information:
    {{context}}

    Please analyze these cell types and markers for {target_species} {tissue_type} annotation with these requirements:

    1. First, list the all relevant broad cell types in {tissue_type} based on the provided information and your knowledge, including:
        - Tissue-specific cells (e.g., Kupffer cells for liver)
        - Broad cell categories, that contain the cell types you listed above.

    2. For each broad cell category, provide a conservative list of canonical markers that would be helpful for annotation.
       Focus on markers that are:
       - Highly specific to the broad cell category
       - Well-conserved across species
       - Functionally important

    3. If there are any more broad cell categories that don't show up in the input but you think are important for annotation, add them to the output. 
    4. For the cell types that are tissue-specific, also list their conservative markers. 
        

    Format your response as a hierarchical list with:
    - Broad cell categories
    - Key markers for each broad cell category
    - Under the broad category, list the tissue specific cell types, and their conservative markers
    - Brief notes on marker reliability and cross-species considerations
    """

    def format_docs(docs):
        text = "\n\n".join(doc.page_content for doc in docs)
        tokens = len(text.split())
        max_tokens = 80000
        if tokens > max_tokens:
            return text[:int(len(text) * (max_tokens / tokens))]
        return text

    # Initialize the retriever
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 2}
    )

    # Initialize the language model based on choice
    if model_choice == 'gpt':
        llm = ChatOpenAI(model="gpt-4o")
    elif model_choice == 'claude':
        llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
    else:
        raise ValueError("Invalid model choice. Choose 'gpt' or 'claude'.")

    # Create the RAG chain
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | PromptTemplate.from_template(MARKER_ANALYSIS_PROMPT)
        | llm
        | StrOutputParser()
    )

    # Execute the analysis
    try:
        print(f"Analyzing {tissue_type} markers for {target_species} using {model_choice} model...")
        result = chain.invoke(f"What are the relevant cell types and markers for {tissue_type}?")
        
        # Save results in tissue subdirectory
        output_dir = f"./{tissue_type}_{target_species}"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{target_species.lower()}_{tissue_type.lower()}_marker_analysis.txt")
        
        with open(output_file, 'w') as f:
            f.write(result)
        
        print(f"\nResults saved to: {output_file}")
        return result
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None



def get_broad_celltypes(tissue_type="Liver", target_species="Human", model_choice='claude'):
    """
    Get lists of broad cell type ontology IDs and names for a tissue.
    
    Args:
        tissue_type (str): Type of tissue
        target_species (str): Species to analyze
        model_choice (str): Choice of language model ('gpt' or 'claude')
        
    Returns:
        tuple: (list of Cell Ontology IDs, list of broad cell type names)
    """
    
    PROMPT = f"""
    You are an expert in biology specializing in {tissue_type} annotation. 
    For {tissue_type} in {target_species}, what are the broad cell types(CATEGORIES) that show up there?
    Example: in lung, we have epithelial cells, supporting cells, etc.
    For each broad cell CATEGORY, what is the corresponding Cell Ontology ID?
    Output format:
    CL:0000000 # broad cell type name
    CL:0000000 # broad cell type name
    IMPORTANT: 
    1. Include only broad categories (no specific subtypes)
    2. Double check each ID is correct
    3. Output ONLY the CL IDs with cell type names as comments
    4. No explanations or additional text
    5. Make sure the name matches exactly what's in Cell Ontology
    """
    try:
        print(f"Identifying broad cell types in {target_species} {tissue_type}...")
        
        if model_choice == 'gpt':
            from openai import OpenAI
            client = OpenAI()
            response = client.chat.completions.create(
                model="gpt-4o",  # Removed 'o' suffix
                messages=[{"role": "user", "content": PROMPT}]
            )
            content = response.choices[0].message.content
        else:  # default to claude
            from anthropic import Anthropic
            anthropic = Anthropic()
            message = anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[{"role": "user", "content": PROMPT}]
            )
            content = message.content[0].text
            
        #print(f"Content: {content}")
        
        # Parse both IDs and names
        cell_ids = []
        cell_names = []
        
        for line in content.split('\n'):
            line = line.strip()
            if line and line.startswith('CL:'):
                parts = line.split('#', 1)  # Split only on first '#'
                if len(parts) == 2:
                    cell_id = parts[0].strip()
                    cell_name = parts[1].strip()
                    cell_ids.append(cell_id)
                    cell_names.append(cell_name)
        
        print(f"Extracted IDs: {cell_ids}")
        print(f"Extracted names: {cell_names}")
        
        return cell_ids, cell_names
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None, None
    
    
    from owlready2 import World
import os
import json

def get_cell_tree(cl_id, tissue_type="Liver", target_species="Human"):
    """
    Generate a cell ontology tree for a given Cell Ontology ID.
    
    Args:
        cl_id (str): Cell Ontology ID
        tissue_type (str): Type of tissue (used for subfolder)
        target_species (str): Species to analyze
        
    Returns:
        dict: A dictionary representing the cell ontology tree
    """
    print("Loading ontology...")
    world = World()
    try:
        onto = world.get_ontology("http://purl.obolibrary.org/obo/cl.owl").load()
        print("Ontology loaded successfully.")
        print(f"Number of classes in ontology: {len(list(onto.classes()))}")
    except Exception as e:
        print(f"Error loading ontology: {str(e)}")
        return None
    
    def get_tree(cls):
        if not hasattr(cls, 'label') or not cls.label:
            print(f"Warning: Class {cls} has no label")
            return None
        children = [get_tree(c) for c in cls.subclasses() if hasattr(c, 'label') and c.label]
        return {
            "name": cls.label.first(),
            "id": cls.name,
            "children": children
        }
    
    print(f"Processing {cl_id}...")
    try:
        cell = None
        for cls in onto.classes():
            if cls.name == cl_id.replace(":", "_"):
                cell = cls
                break
        
        if cell is not None:
            print(f"Found class: {cell}")
            tree = get_tree(cell)
            if tree is None:
                print(f"Warning: Unable to create tree for {cl_id}")
            else:
                print(f"Tree created for {cl_id}")
            return tree
        else:
            print(f"Error: Class not found for {cl_id}")
            return None
    except Exception as e:
        print(f"Error accessing {cl_id}: {str(e)}")
        return None

def print_tree(tree, file=None, indent=0):
    if tree is None:
        return
    line = "  " * indent + f"{tree['name']} ({tree['id']})"
    print(line)
    if file:
        file.write(line + "\n")
    for child in tree['children']:
        print_tree(child, file, indent + 1)

def save_cell_tree(tree, cl_id, tissue_type="Liver", target_species="Human"):
    """
    Save a cell tree to files in the tissue subfolder.
    
    Args:
        tree (dict): A dictionary representing the cell ontology tree
        cl_id (str): Cell Ontology ID
        tissue_type (str): Type of tissue (used for subfolder)
    """
    if not tree:
        print("No tree was generated. Exiting.")
        return

    # Create tissue subfolder if it doesn't exist
    os.makedirs(f"./{tissue_type}_{target_species}/Ontology", exist_ok=True)
    
    # Define filenames
    filename = f"./{tissue_type}_{target_species}/Ontology/{cl_id}.txt"
    json_filename = f"./{tissue_type}_{target_species}/Ontology/{cl_id}.json"

    try:
        # Save detailed tree to text file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Cell Ontology Tree\n")
            f.write("=" * 80 + "\n\n")
            
            header = f"\nTree for {cl_id}:"
            print(header)
            f.write(header + "\n")
            print_tree(tree, f)
            f.write("\n" + "-" * 40 + "\n")
        
        # Save as JSON for programmatic access
        with open(json_filename, 'w', encoding='utf-8') as json_f:
            json.dump(tree, json_f, indent=2)

        print(f"\nTree has been saved to {filename} and {json_filename}")
        
    except Exception as e:
        print(f"Error writing to file: {str(e)}")


import ast
import re
from typing import List

def generate_specialized_search_terms(cell_type: str, target_tissue: str, llm) -> List[str]:
    """
    Generate specialized search terms for cell types using LLM to find relevant subtypes in a cell ontology tree.
    
    Args:
        cell_type: The type of cell to analyze (root of ontology tree)
        target_tissue: The target tissue context
        llm: Language model instance to use
    
    Returns:
        List of relevant search terms for filtering the ontology
        
    Raises:
        ValueError: If unable to generate valid search terms
    """
    search_terms_prompt = f"""As an expert in {cell_type} biology and {target_tissue} anatomy, generate some search terms to find relevant {cell_type} subtypes in {target_tissue}.

Task: Create search terms that will help us find the most relevant subtypes of {cell_type} cells within {target_tissue} from a broad cell ontology tree with parent root as {cell_type}. 

Consider:
1. key words for major subtypes of {cell_type}s specifically found in {target_tissue}
2. key words for key anatomical classifications in {target_tissue}
3. key words for primary functional classifications relevant to {target_tissue}

CRITICAL OUTPUT FORMAT:
RETURN ONLY A PYTHON LIST LIKE THIS, NOTHING ELSE:
["term1", "term2", "term3"]

Requirements:
- Must be in format: ["term1", "term2", "term3"]
- Each term in double quotes, comma-separated
- Terms must relate to {target_tissue} {cell_type}

Examples for different cells:
For fibroblasts in heart: ["ventricular fibroblast", "epicardial derived", "valve interstitial", "activated myofibroblast", "atrial fibroblast", "endocardial fibroblast"]
For macrophages in liver: ["kupffer cell", "sinusoidal", "phagocytic", "portal"]
"""

    try:
        # Generate terms using LLM
        chain = PromptTemplate.from_template(search_terms_prompt) | llm | StrOutputParser()
        result = chain.invoke({}).strip()
        
        # Try to extract a valid Python list if the format isn't perfect
        def extract_terms(text):
            # First try to find a proper Python list
            list_pattern = r'\[(.*?)\]'
            matches = re.findall(list_pattern, text)
            
            if matches:
                # Take the first match that looks like a proper list
                for match in matches:
                    try:
                        terms = ast.literal_eval(f"[{match}]")
                        if isinstance(terms, list) and all(isinstance(x, str) for x in terms):
                            return terms
                    except:
                        continue
            
            # If no valid list found, try to extract quoted strings
            quoted_pattern = r'"([^"]*)"'
            terms = re.findall(quoted_pattern, text)
            if terms:
                return terms
                
            # If still no terms, split by common separators
            if not terms:
                # Remove common list-like characters and split
                cleaned = text.replace('[', '').replace(']', '').replace('"', '').replace("'", '')
                terms = [t.strip() for t in re.split(r'[,\n]', cleaned) if t.strip()]
                
            return terms
        
        # Try to parse the result multiple ways
        try:
            terms = ast.literal_eval(result)
        except:
            terms = extract_terms(result)
            
        # Process and validate terms
        processed_terms = []
        for term in terms:
            term = term.strip().lower()
            # Validate term length (1-4 words)
            if 1 <= len(term.split()) <= 4:
                processed_terms.append(term)
                
        # Remove duplicates while preserving order
        processed_terms = list(dict.fromkeys(processed_terms))
        
        # Ensure base cell type is included
        base_cell_type = cell_type.lower()
        if base_cell_type not in processed_terms:
            processed_terms.insert(0, base_cell_type)
            
        # Sort by specificity (length) and limit to top terms
        processed_terms.sort(key=len, reverse=True)
        final_terms = processed_terms[:10]
        
        print(f"Generated {len(final_terms)} search terms: {final_terms}")
        
        if not final_terms:
            raise ValueError("No valid terms generated")
            
        return final_terms
        
    except Exception as e:
        error_msg = f"Error generating search terms: {str(e)}"
        print(error_msg)
        raise ValueError(error_msg)
    
    
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
import os
import concurrent.futures
from typing import List, Tuple, Optional
from dataclasses import dataclass
from tqdm import tqdm
import time
from functools import partial

@dataclass
class ProcessingResult:
    cell_id: str
    cell_name: str
    success: bool
    error_message: Optional[str] = None
    output_file: Optional[str] = None

def create_llm(model_choice='claude'):
    """Create LLM instance with appropriate settings."""
    if model_choice == 'gpt':
        return ChatOpenAI(
            model="gpt-4o", 
            max_tokens=2000,
            request_timeout=60
        )
    elif model_choice == 'claude':
        return ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            timeout=60
        )
    
def process_single_cell_type(
    cell_info: Tuple[str, str],
    base_dir: str,
    tissue_type: str,
    model_choice: str
) -> ProcessingResult:
    """Process a single cell type with proper error handling."""
    cell_id, cell_name = cell_info
    
    try:
        input_file = os.path.join(base_dir, "Ontology", f"{cell_id}.txt")
        
        if not os.path.exists(input_file):
            return ProcessingResult(
                cell_id=cell_id,
                cell_name=cell_name,
                success=False,
                error_message=f"Ontology file not found"
            )

        # Create new LLM instance for each worker to avoid sharing
        llm = create_llm(model_choice)
        
        print(f"\nProcessing {cell_name} ({cell_id})...")
        
        # Generate search terms with clear printing
        search_terms = generate_specialized_search_terms(cell_name, tissue_type, llm)
        print(f"\nGenerated base search terms for {cell_name}:")
        for i, term in enumerate(search_terms, 1):
            print(f"  {i}. {term}")
            
        # Add tissue-specific terms
        tissue_terms = [f"{term} {cell_name}" for term in tissue_type.lower().split()]
        search_terms.extend(tissue_terms)
        
        if tissue_terms:
            print(f"\nAdded tissue-specific terms:")
            for i, term in enumerate(tissue_terms, len(search_terms) - len(tissue_terms) + 1):
                print(f"  {i}. {term}")
                
        print(f"\nTotal {len(search_terms)} search terms will be used for retrieval")
        print("-" * 50)
        
        # Rest of the function remains the same...
        # Read and process ontology file
        with open(input_file, 'r') as f:
            ontology_content = f.read()
            
        # Split text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200,
            separators=["\nTree for", "\n  ", "\n    ", "\n"]
        )
        
        splits = text_splitter.split_documents([Document(page_content=ontology_content)])
        
        # Create vector store
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings
        )
        
        retriever = vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 3,
                "score_threshold": 0.6
            }
        )
        
        # Process search terms
        all_results = []
        for term in search_terms:
            try:
                results = retriever.get_relevant_documents(term)
                all_results.extend(results)
                # Add small delay to avoid rate limits
                time.sleep(0.1)
            except Exception as e:
                print(f"Error retrieving results for term '{term}': {str(e)}")
                continue
                
        # Dedup results
        seen = set()
        unique_results = []
        for doc in all_results:
            content_hash = hash(doc.page_content)
            if content_hash not in seen:
                seen.add(content_hash)
                unique_results.append(doc)
                
        # Process with LLM
        prompt_template = f"""As a {cell_name} expert, identify cells in this ontology section that:
        1. Are found in {tissue_type}
        2. Have known {tissue_type} functions
        
        Context: {{context}}
        
        Requirements:
        1. Keep Cell Ontology IDs and hierarchy
        2. Include parent cells if relevant
        3. OUTPUT ONLY contain the tree, NO other text.
        4. ONLY FOCUS ON {cell_name}, output only {cell_name}, no other text.
        
        Format as a tree. If no relevant cells found, return plain empty text."""
        
        final_results = []
        for chunk in unique_results:
            try:
                chain = PromptTemplate.from_template(prompt_template) | llm | StrOutputParser()
                result = chain.invoke({"context": chunk.page_content})
                
                if result and result.strip():
                    final_results.append(result)
                    
            except Exception as e:
                print(f"Error processing chunk for {cell_name}: {str(e)}")
                continue
                
        # Save results
        if final_results:
            refined_dir = os.path.join(os.path.dirname(os.path.dirname(input_file)), "refined_ontology")
            os.makedirs(refined_dir, exist_ok=True)
            
            output_file = os.path.join(refined_dir, f"{tissue_type}_{cell_name}.txt")
            
            with open(output_file, 'w') as f:
                f.write(f"{tissue_type} {cell_name} Ontology\n")
                f.write("=" * 80 + "\n\n")
                f.write("\n\n".join(final_results))
                
            return ProcessingResult(
                cell_id=cell_id,
                cell_name=cell_name,
                success=True,
                output_file=output_file
            )
        else:
            return ProcessingResult(
                cell_id=cell_id,
                cell_name=cell_name,
                success=True,
                error_message="No relevant cells found"
            )
            
    except Exception as e:
        return ProcessingResult(
            cell_id=cell_id,
            cell_name=cell_name,
            success=False,
            error_message=str(e)
        )
        
        
        
def process_tissue_ontology_parallel(
    tissue_type: str,
    target_species: str,
    model_choice: str = 'claude',
    max_workers: int = 3, 
    cell_ids: Optional[List[str]] = None,
    cell_names: Optional[List[str]] = None
) -> List[ProcessingResult]:
    """
    Process all cell types for a tissue in parallel with controlled concurrency.
    
    Args:
        tissue_type: Type of tissue to analyze
        target_species: Target species for analysis
        model_choice: Which LLM to use ('claude' or 'gpt')
        max_workers: Maximum number of parallel workers
    
    Returns:
        List of ProcessingResult objects containing results and errors
    """  
        # Setup base directory
    base_dir = f"./{tissue_type}_{target_species}"
    os.makedirs(os.path.join(base_dir, "refined_ontology"), exist_ok=True)
        
    print(f"\nProcessing {len(cell_ids)} cell types for {tissue_type} in {target_species}")
        
    # Prepare partial function with fixed arguments
    process_func = partial(
        process_single_cell_type,
        base_dir=base_dir,
        tissue_type=tissue_type,
        model_choice=model_choice
    )
    
    # Process in parallel with progress bar
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Create futures
        future_to_cell = {
            executor.submit(process_func, (cell_id, cell_name)): (cell_id, cell_name)
            for cell_id, cell_name in zip(cell_ids, cell_names)
        }
        
        # Process with progress bar
        with tqdm(total=len(cell_ids), desc="Processing cell types") as pbar:
            for future in concurrent.futures.as_completed(future_to_cell):
                cell_id, cell_name = future_to_cell[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append(ProcessingResult(
                        cell_id=cell_id,
                        cell_name=cell_name,
                        success=False,
                        error_message=str(e)
                    ))
                pbar.update(1)
    
    # Print summary
    successful = sum(1 for r in results if r.success)
    failed = sum(1 for r in results if not r.success)
    print(f"\nProcessing complete: {successful} successful, {failed} failed")
    
    # Print errors if any
    if failed > 0:
        print("\nErrors encountered:")
        for result in results:
            if not result.success:
                print(f"- {result.cell_name} ({result.cell_id}): {result.error_message}")
    
    return results



def combine_ontologies(tissue_type="Lung", target_species="Fetal", model_choice='claude'):
    """
    Combine and refine all processed ontology files into a complete tree.
    """
    input_dir = f"./{tissue_type}_{target_species}/refined_ontology"
    output_file = f"./{tissue_type}_{target_species}/final_ontology.txt"

    # Initialize the language model
    if model_choice == 'gpt':
        llm = ChatOpenAI(model="gpt-4o", api_key=os.environ["OPENAI_API_KEY"])
    elif model_choice == 'claude':
        llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", api_key=os.environ["ANTHROPIC_API_KEY"], max_tokens=8000)

    # Create prompt template
    combine_prompt = PromptTemplate.from_template("""You are an expert in {tissue_type} biology and cell annotation. 
        You have been given multiple refined cell ontology trees pieces for {target_species} {tissue_type}.

        Your task is to:
        0. Organize the pieces into a complete ontology tree
        1. VERY IMPORTANT: PLEASE KEEP ALL the DETAILS OF MY INPUT PIECES, JUST ORDER AND ARRANGE THEM BETTER. 
        2. Especially for the subtypes that are from a broad cell type that are consider very abundant in the tissue, for the detailed cell types, think if there are any more cell types in the same parent group that you can add in. MAKE SURE BE AS DETAILED AS POSSIBLE, DOUBLE CHECK IF ANY THING IS MISSING.
        3. Add in more detail cells to create a very COMPLETE cell ontology tree specific to {tissue_type}, and ONLY remove the cell types that are not found in {tissue_type}.
        4. Do NOT limit yourself to just the provided trees - use your knowledge of {tissue_type} cell types to expand the ontology tree if anything is missing.
        5. Organize cells in a hierarchical tree structure, with parent cells and sub cells based on ontology hierarchy and function and biological relationships. If there are some interchangeable names, list there. 
        6. Expand on cell types that are abundant or crucial in this specific tissue
        7. For the broad cell types that are less common in {tissue_type}, give broader subcategories for them, but still keep the tissue specific cell highlight.
        7. Ensure the hierarchy reflects tissue-specific organization
        8. SOME TIMES SOME CELL'S NAME ARE INTERCHANGEABLE, YOU ALSO PUT ALTERNATIVE NAMES FOR THEM IN COMMENTS.

        Here are the ontology trees to consider:
        {context}

        Format your response as:
        cell_type (ID)  // annotation about function, markers, location
            subcell_type (ID)  // specific annotation

        IMPORTANT: 
        - Focus on the most relevant and abundant cell types for {tissue_type}
        - Include ALL major cell populations known to be present
        - Don't restrict output to just the provided trees
        - Use tissue-specific knowledge to guide the hierarchy
        - After you generate the tree, double check if there are any cell types missing, if so, add them in. Frequently some of cell types at depth 2, 3,4 in the ontology tree are missing.
        """)

    try:
        print(f"Loading refined ontologies from {input_dir}...")
        
        # Load and combine all files
        all_content = []
        for filename in os.listdir(input_dir):
            if filename.endswith('.txt'):
                with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as f:
                    all_content.append(f.read())
        
        combined_content = "\n\n".join(all_content)
        
        print("Processing combined ontologies...")
        
        # Create simple chain
        chain = combine_prompt | llm | StrOutputParser()
        
        # Process with combined content
        result = chain.invoke({
            "tissue_type": tissue_type,
            "target_species": target_species,
            "context": combined_content
        })
        
        # Save result
        with open(output_file, 'w') as f:
            f.write(result)
        
        print(f"Final annotated ontology saved to: {output_file}")
        
    except Exception as e:
        print(f"An error occurred while combining ontologies: {str(e)}")
        import traceback
        traceback.print_exc()
        

from langchain_community.document_loaders import TextLoader
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

def analyze_cell_patterns(tissue_type="Liver", target_species="Human", model_choice='claude'):
    """
    Analyze cell type patterns from refined ontology.
    
    Args:
        tissue_type (str): Type of tissue to analyze
        target_species (str): Species to analyze
        model_choice (str): Choice of language model ('gpt' or 'claude', default is 'claude')
    """
    
    # Initialize the language model based on choice
    if model_choice == 'gpt':
        llm = ChatOpenAI(model="gpt-4o", api_key=os.environ["OPENAI_API_KEY"])
    else:  # default to claude
        llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022", 
            api_key=os.environ["ANTHROPIC_API_KEY"],
            max_tokens=4096  # Adjust based on your needs
        )

    # Load the refined ontology
    loader = TextLoader(f'./{tissue_type}_{target_species}/final_ontology.txt', encoding='utf-8')
    docs = loader.load()
    cell_hierarchy = docs[0].page_content

    # Create a prompt for analyzing cell type patterns
    CELL_PATTERN_PROMPT = """
    You are an expert in developmental biology and cell type analysis. Given this {tissue_type} cell hierarchy in {target_species}:

    {cell_hierarchy}

    Task: Analyze these cell types to identify major organizational principles and grouping patterns.

    Please:
    1. Identify 2-6 major organizing principles for these {tissue_type} cells in {target_species} (like location, function, developmental stage, etc.)
    IMPORTANT NOTE: There will be some broad cell types that has lots of sub cell types shows up in our tissue, and lots of sub principles related to this broad cell type, you can list more if you need and have sub principles under the major principles (like a tree structure), if you think this major category is important and show up a lot in this tissue. 
    EXAMPLE 1 FOR IMPORTANT NOTE: in heart tissues, we have lots of fibroblast types, fibroblasts can be categorized using: Location: Chamber Identity (Ventricle/Atria), Layer Identity (Epi/Myo/Endocardial), Region Identity (Valve/Septal) and lots of other sub categories like activation states (quiescent/activated) or developmental origin.
    EXAMPLE OUTPUT FOR IMPORTANT NOTE JUST FOR FIBROBLAST in heart tissues, heart tissue will have other cell types as well, but fibroblast is a good example, and other broad cell types if don't have lots of subcategories, you can just use some broad categories to describe them, BUT, IF A BROAD CELLTYPE IS LIKE FIBROBLAST IN HEART, DO AS MUCH SUB CATEGORIZATION AS POSSIBLE, YOU CAN HAVE SUBCATEGORIES UNDER THE SUBCATEGORIES, AND EVEN SUB SUBCATEGORIES:
    
    ## 1. ANATOMICAL LOCATION
    Primary division of cardiac fibroblasts based on anatomical location
    ### Main Groups:
    A. Chamber Identity
    - Core markers: nppa, myl2, myl7
    - Sub-principles:
    * Ventricular
        - Left: irx2, irx4, hand1
        - Right: hand2, mef2c
        - Septal: tbx5, irx2
    * Atrial
        - Left: pitx2, meis2
        - Right: tbx5, hcn4
        
    B. Layer Identity
    - Core markers: tcf21, pdgfra, thy1
    - Sub-principles:
    * Epicardial-derived
        - wt1, tbx18, aldh1a2
    * Myocardial
        - ddr2, col1a1, col1a2
    * Endocardial-derived
        - nfatc1, npr3, endoglin

    ## 2. DEVELOPMENTAL ORIGIN
    ### Main Groups:
    A. Epicardial-derived
    - Core markers: wt1, tbx18
    - Migration states:
    * EMT markers: snai1, snai2, twist1
    * Invasion markers: mmp2, mmp14

    B. Endocardial-derived
    - Core markers: nfatc1, npr3
    - EndoMT markers: tgfb1, tgfb2, snai1

    ## 3. FUNCTIONAL STATE
    ### Main Groups:
    A. Quiescent State
    - Core markers: pdgfra, tcf21
    - Sub-types:
    * Homeostatic: dpp4, cd90
    * Matrix-maintaining: col1a1, col3a1

    B. Activated State
    - Core markers: acta2, postn
    - Activation markers:
    * Mechanical: tnc, postn
    * Inflammatory: il6, ccl2
    * Fibrotic: tgfb1, ctgf

    ## 4. REGIONAL SPECIALIZATION
    ### Main Groups:
    A. Valve-associated
    - Core markers: sox9, twist1
    - Valve types:
    * Atrioventricular: tbx20, msx1
    * Semilunar: klf2, klf4

    B. Conduction System-associated
    - Core markers: tbx3, hcn4
    - Regions:
    * SA node: tbx3, hcn4
    * AV node: tbx3, cacna1g

    ## 5. DISEASE-ASSOCIATED STATES
    ### Main Groups:
    A. Injury Response
    - Core markers: postn, acta2
    - Sub-types:
    * Scar-forming: col1a1, fn1
    * Inflammatory: il1b, tnf

    B. Pathological Remodeling
    - Core markers: ctgf, tgfb1
    - Sub-types:
    * Fibrotic: col1a1, col3a1
    * Hypertrophic: nppa, nppb
    
    EXAMPLE 2: in human liver, for BROAD PRINCIPLES, here is a example. 
    ## 1. MAJOR ORGANIZING PRINCIPLES

    A. ANATOMICAL LOCATION
    Main Groups:
    - Portal Triad Zone (Zone 1)
    - Midzonal Region (Zone 2)
    - Central Vein Zone (Zone 3)
    Biological Significance: Zonation reflects metabolic specialization and oxygen gradient
    Key Markers:
    * Portal Zone: AXIN2, CYP2E1low, GLULlow
    * Midzonal: PCKlow, CYP2E1mid
    * Central: GLULhigh, CYP2E1high, LYVE1high

    B. CELL LINEAGE
    Main Groups:
    - Epithelial (Parenchymal)
    - Mesenchymal
    - Immune Resident
    Biological Significance: Reflects developmental origin and primary functions
    Key Markers:
    * Epithelial: ALB, HNF4A, KRT8/18
    * Mesenchymal: PDGFRA, PDGFRB, DCN
    * Immune: CD45, CD68, CD3E

    C. FUNCTIONAL STATE
    Main Groups:
    - Metabolic Processing
    - Immune Surveillance
    - Structural Support
    - Bile Transport
    Biological Significance: Defines role in liver homeostasis
    Key Markers:
    * Metabolic: ALB, CYP3A4, G6PC
    * Immune: CD68, CD163, CLEC4F
    * Structural: COL1A1, ACTA2, TIMP1
    * Bile Transport: ABCB11, ABCC2, SLC10A1

    ## 2. DETAILED ANALYSIS FOR MAJOR CELL GROUPS WITH SUB-PRINCIPLES

    HEPATOCYTES (Major Focus Group)
    Sub-Principles:
    a) Zonation-Based:
    - Periportal: PCK1, ALDOB, HAL
    - Midzone: CYP2E1mid, ALB, TDO2
    - Pericentral: GLUL, CYP2E1high, LRG5

    b) Metabolic State:
    - Gluconeogenic: PCK1, G6PC, FBP1
    - Lipogenic: FASN, ACACA, SCD
    - Xenobiotic: CYP3A4, CYP2E1, CYP1A2

    c) Functional Status:
    - Homeostatic: ALB, TTR, APOA1
    - Stress Response: MT1/2, HSPA5, XBP1
    - Regenerative: PCNA, CCND1, MKI67

    SINUSOIDAL CELLS
    Sub-Principles:
    a) Cell Type Specialization:
    - LSECs: PECAM1, LYVE1, CD34
    - Kupffer Cells: CD68, CLEC4F, CD163
    - Stellate Cells: PDGFRB, LRAT, DES

    b) Activation State:
    - Quiescent: LRAT, RELN, NGFR
    - Activated: ACTA2, COL1A1, TIMP1
    - Inflammatory: IL1B, TNF, CCL2

    ## 3. CELLS WITH MULTIPLE GROUP MEMBERSHIP

    - Hepatic Stellate Cells:
    * Location: Space of Disse
    * Functions: Vitamin A storage, ECM production, regeneration
    Markers: PDGFRB, LRAT, DES, VIM

    - Liver-Resident NK cells:
    * Location: Sinusoids and space of Disse
    * Functions: Immune surveillance, tissue homeostasis
    Markers: CD56, CXCR6, CD69

    ## 4. DISEASE-RELEVANT STATES

    A. Fibrosis-Associated:
    - Activated stellate cells: ACTA2, COL1A1, TIMP1
    - Inflammatory macrophages: TNF, IL1B, CCL2
    - Stress-response hepatocytes: HSPA5, XBP1, ATF4

    B. Regeneration-Associated:
    - Proliferating hepatocytes: PCNA, MKI67, CCND1
    - Progenitor cells: KRT19, EPCAM, SOX9
    - Supporting niche: HGF, WNT, NOTCH
    
    
    2. For each principle:
    - List the main groups under this principle
    - Explain why this grouping is biologically meaningful
    3. Note any cells that could belong to multiple groups and explain why
    4. Consider both developmental and functional aspects in your grouping
    5. For each major group, provide a conservative list of 1-5 key markers that are:
    - Highly specific to that group
    - Well-conserved across species
    - Functionally important
    
    6. IMPORTANT: For each major group, if we have case similar like EXAMPLE 1, provide a detail list of markers for each sub principle. And think about a complete list of sub principles for this major group. This time for sub principles, you can provide a much longer marker list that you are confidence in. 
    7. Don't restrict yourself to the ontology tree, if you think there are some cell types principles (either major or sub) missing, you can add them in. 
    8. Think about our species, if mouse then it should be lower case in gene name, if human then it should be upper case in gene name. 

    Format your response in a clear, structured way that could help inform cell type annotation and analysis.
    Focus on patterns that would be most useful for single-cell analysis.

    IMPORTANT: Provide your response in txt format for better readability.
    """

    # Create the prompt template
    prompt = PromptTemplate(
        template=CELL_PATTERN_PROMPT,
        input_variables=["tissue_type", "target_species", "cell_hierarchy"]
    )

    # Create the chain
    chain = (
        prompt 
        | llm 
        | StrOutputParser()
    )

    # Execute the analysis
    try:
        print(f"Analyzing {tissue_type} cell type patterns using {model_choice} model...")
        result = chain.invoke({
            "tissue_type": tissue_type,
            "target_species": target_species,
            "cell_hierarchy": cell_hierarchy
        })
        
        # Save results in tissue subdirectory
        os.makedirs(f"{tissue_type}_{target_species}", exist_ok=True)
        output_file = f"./{tissue_type}_{target_species}/cell_type_patterns.txt"
        with open(output_file, 'w') as f:
            f.write(result)
            
        print(f"\nResults saved to: {output_file}")
        return result
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return None




def create_final_summary(tissue_type, target_species, reference_species="Human"):
    """
    Combine all analysis files with connecting sentences.
    
    Args:
        tissue_type (str): Type of tissue analyzed
        target_species (str): Species analyzed
        reference_species (str): Reference species for comparison
    """
    
    base_dir = f"./{tissue_type}_{target_species}"
    print(base_dir)
    output_file = f"{base_dir}/summary.txt"
    
    try:
        # Initialize the summary content
        summary_content = [
            f"# You are analyzing {target_species} {tissue_type}\n",
            f"## I have some information about the cell types in this tissue based on {reference_species} reference data. You can use this information to help you understand the cell types in this tissue. But note that the additional information is just for your reference, don't force your self so much to align with it. And IMPORTANT: If your analyzed species is not the same as reference, like tiger vs human, fetal vs human, you think about how to use the information carefully to take the difference into account.\n",
            f"Ok here is my info based on {reference_species} {tissue_type}\n\n",
            
            "## 1. Cell Type Markers\n",
            f"Those are broad some cell types might show up in {reference_species} {tissue_type}, and their conservative markers:\n\n"
        ]
        
        # Add marker analysis content
        with open(f"{base_dir}/{target_species.lower()}_{tissue_type.lower()}_marker_analysis.txt", 'r') as f:
            summary_content.append(f.read() + "\n\n")
            
        # Add ontology tree section
        summary_content.extend([
            "## 2. Cell Ontology Tree\n",
            f"Below is the refined cell ontology hierarchy showing the relationships between different cell types that might be present in {reference_species} {tissue_type}, note that, this might not be a complete list of cell types in {target_species} {tissue_type}, and our data might not cover all of them, and keep in mind the species you are analyzing, {target_species}:\n\n"
        ])
        
        # Add ontology content
        print(f"{base_dir}/final_ontology.txt")
        with open(f"{base_dir}/final_ontology.txt", 'r') as f:
            summary_content.append(f.read() + "\n\n")
        
        # Add cell pattern analysis
        summary_content.extend([
            "## 3. Cell Type Pattern Analysis\n",
            f"Analysis of major organizing principles and cell type patterns in {target_species} {tissue_type}:\n\n",
            "VERY IMPORTANT: When you encounter some cell type that shows up a lot in the tissue, and has lots of subcategories, you use the subcategories to help you do the most detail you can. For example:in heart tissues, we have lots of fibroblast types, fibroblasts can be categorized using: Location: Chamber Identity (Ventricle/Atria), Layer Identity (Epi/Myo/Endocardial), Region Identity (Valve/Septal) and lots of other sub categories like activation states (quiescent/activated) or developmental origin. Then you can label like: Location+Layer+Region+other subcategories. . use similar logic here. Do detail and complete if you can (and you decide on whether this annotation should be that detail based on general knowledge about the tissue and that cell type, for example in the fibroblast in heart people tend to do detail annotation, while in some other tissue people tend to do less detail on fibroblast, etc), and if you decided on detail annotation,  put this DETAILED version in the FIRST subtype of your prediction if you think it make sense, but if you are not having enough evidence, then trust yourself THE LOGIC IS: those subcategories are PCA like thing, cells can be in multiple categories, each are a aspect of characteristing things. YOU MAKE DECISION ON whether a cell should be in multiple categories based on your biological knowledge.\n\n"
        ])
        
        with open(f"{base_dir}/cell_type_patterns.txt", 'r') as f:
            summary_content.append(f.read() + "\n\n")
            
        # Write the combined content
        with open(output_file, 'w') as f:
            f.write(''.join(summary_content))
            
        print(f"Summary created successfully: {output_file}")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find one of the required files - {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        

def create_additional_considerations(tissue_type, target_species, reference_species="Human", model_choice='claude'):
    """
    Generate additional considerations for cross-species analysis.
    
    Args:
        tissue_type (str): Type of tissue analyzed
        target_species (str): Species analyzed
        reference_species (str): Reference species for comparison
        model_choice (str): Choice of language model ('gpt' or 'claude')
    """
    
    # Initialize the language model
    if model_choice == 'gpt':
        llm = ChatOpenAI(model="gpt-4o", api_key=os.environ["OPENAI_API_KEY"])
    else:  # default to claude
        llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022", 
            api_key=os.environ["ANTHROPIC_API_KEY"]
        )

    # Create prompt for additional considerations
    considerations_prompt = """Since we are using {reference_species} to help annotate {target_species} in {tissue_type}, 
    think about some key differences that might affect annotation.

    Please consider and explain:
    1. Developmental differences if comparing across life stages
    2. Species-specific anatomical or functional adaptations
    3. Marker gene conservation and expression differences
    4. Cell state and population differences
    5. Technical considerations for annotation

    For example:
    - Fetal data will have developmental processes and transitional states
    - Different mammals might have tissue-specific adaptations
    - Some markers might not be conserved across species
    - Cell proportions and states might vary

    Format your response in txt with clear sections and examples.
    For each major point, give some markers. 
    Focus on practical implications for cell type annotation.
    """

    # Create the prompt template
    prompt = PromptTemplate(
        template=considerations_prompt,
        input_variables=["tissue_type", "target_species", "reference_species"]
    )

    # Create the chain
    chain = (
        prompt 
        | llm 
        | StrOutputParser()
    )

    try:
        print(f"Generating additional considerations for {target_species} {tissue_type}...")
        
        # Generate the analysis
        result = chain.invoke({
            "tissue_type": tissue_type,
            "target_species": target_species,
            "reference_species": reference_species
        })
        
        # Save to file
        base_dir = f"./{tissue_type}_{target_species}"
        output_file = f"{base_dir}/additional_considerations.txt"
        
        with open(output_file, 'w') as f:
            f.write(result)
            
        print(f"Additional considerations saved to: {output_file}")
        return result
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
    
def clean_summary(tissue_type, target_species, compare=True, reference_species="Human"):
    """
    Read summary file and additional considerations (if compare=True),
    merge them and remove markdown code block symbols. Also, remove subfolders in the main folder.
    
    Args:
        tissue_type (str): Type of tissue analyzed
        target_species (str): Species analyzed
        compare (bool): Whether to include additional considerations
    """
    import os
    import shutil

    try:
        # Define file paths
        base_dir = f"./{tissue_type}_{target_species}"
        summary_file = f"{base_dir}/summary.txt"
        considerations_file = f"{base_dir}/additional_considerations.txt"
        output_file = f"{base_dir}/summary_clean.txt"
        
        print(f"Cleaning markdown symbols from files...")
        
        # Read and clean summary file
        with open(summary_file, 'r') as f:
            content = f.read()
            
        # If compare is True, append additional considerations
        if compare:
            try:
                with open(considerations_file, 'r') as f:
                    content += f"\n\n## 4. VERY IMPORTANT: Since we're analyzing {target_species} {tissue_type}, and are using lots of {reference_species} {target_species} info here, therefore it is important to think about the differences between {target_species} and {reference_species}. \n\n"
                    content += f.read()
            except FileNotFoundError:
                print(f"Warning: Additional considerations file not found at {considerations_file}")
        
        # Remove code block symbols
        cleaned_content = content.replace('```', '')
        
        # Write cleaned content
        with open(output_file, 'w') as f:
            f.write(cleaned_content)
            
        print(f"Cleaned summary saved to: {output_file}")

        # Remove subfolders in the main folder
        for item in os.listdir(base_dir):
            item_path = os.path.join(base_dir, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                #print(f"Removed subfolder: {item_path}")

    except FileNotFoundError:
        print(f"Error: Could not find summary file at {summary_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()




import shutil
def run_complete_analysis(tissue_type, target_species, reference_species="Human", model_choice='claude', compare=True, db_path="~/Canonical_Marker (1).csv", max_workers=8):
    """
    Run complete analysis pipeline from marker analysis to final summary.
    
    Args:
        tissue_type (str): Type of tissue to analyze
        target_species (str): Species to analyze
        reference_species (str): Reference species for comparison
        model_choice (str): Choice of language model ('gpt' or 'claude')
        compare (bool): Whether to generate additional cross-species considerations
    """
    try:
        print(f"\n{'='*80}")
        print(f"Starting complete analysis for {target_species} {tissue_type}")
        print(f"{'='*80}\n")

        # Create directory if it doesn't exist
        base_dir = f"./{tissue_type}_{target_species}"
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)  # Remove directory and all its contents
        os.makedirs(base_dir)  # Create new directory

        # Step 1: Get tissue markers
        print("\n1. Analyzing tissue markers...")
        get_tissue_markers(
            tissue_name=tissue_type,
            species_name=target_species,
            file_path=db_path
        )
        
        analyze_tissue_markers(
            csv_path=f"{base_dir}/{tissue_type.lower()}_{target_species.lower()}_celltypes_markers.csv",
            tissue_type=tissue_type,
            target_species=target_species,
            model_choice=model_choice
        )

        # Step 2: Analyze and refine tissue ontology
        print("\n2. Analyzing tissue ontology...")
        
        cell_ids, cell_names = get_broad_celltypes(tissue_type, target_species, model_choice)
        
        for cl_id in cell_ids:
            print(f"Processing {cl_id}...")
            tree = get_cell_tree(cl_id, tissue_type=tissue_type, target_species=target_species)
            save_cell_tree(tree, cl_id, tissue_type=tissue_type, target_species=target_species)  

        process_tissue_ontology_parallel(
            tissue_type=tissue_type,
            target_species=target_species,
            model_choice=model_choice, 
            cell_ids=cell_ids,
            cell_names=cell_names, 
            max_workers=max_workers
        )

        # Step 3: Combine ontologies
        print("\n3. Combining ontologies...")
        combine_ontologies(
            tissue_type=tissue_type,
            target_species=target_species,
            model_choice=model_choice
        )

        # Step 4: Analyze cell patterns
        print("\n4. Analyzing cell patterns...")
        patterns = analyze_cell_patterns(
            tissue_type=tissue_type,
            target_species=target_species,
            model_choice=model_choice
        )

        # Step 5: Create final summary
        print("\n5. Creating final summary...")
        create_final_summary(
            tissue_type=tissue_type,
            target_species=target_species,
            reference_species=reference_species
        )

        # Step 6: Generate additional considerations (optional)
        if compare:
            print("\n6. Generating additional considerations...")
            create_additional_considerations(
                tissue_type=tissue_type,
                target_species=target_species,
                reference_species=reference_species,
                model_choice=model_choice
            )
            print(f"\n{'='*80}")
            print(f"Analysis complete! Check the {tissue_type}_{target_species} directory for results:")
            print(f"1. {tissue_type.lower()}_{target_species.lower()}_marker_analysis.txt")
            print(f"2. final_ontology.txt")
            print(f"3. cell_type_patterns_claude.txt")
            print(f"4. summary.txt")
            print(f"5. additional_considerations.txt")
        else:
            print(f"\n{'='*80}")
            print(f"Analysis complete! Check the {tissue_type}_{target_species} directory for results:")
            print(f"1. {tissue_type.lower()}_{target_species.lower()}_marker_analysis.txt")
            print(f"2. final_ontology.txt")
            print(f"3. cell_type_patterns_claude.txt")
            print(f"4. summary.txt")
        print(f"{'='*80}\n")
        
        # Step 7: Clean summary file
        print("\n Final step. Cleaning summary file...")
        clean_summary(
            tissue_type=tissue_type,
            target_species=target_species,
            compare=compare,
            reference_species=reference_species
        )

    except Exception as e:
        print(f"An error occurred in the analysis pipeline: {str(e)}")
        import traceback
        traceback.print_exc()
        
        

