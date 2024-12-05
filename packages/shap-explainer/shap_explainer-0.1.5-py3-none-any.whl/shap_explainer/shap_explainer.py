from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.document_loaders import TextLoader
import numpy as np
import warnings
import json
import os

def shap_to_json(features, shap_values, num_bins=10):
    # Create a dictionary to hold the data
    data = {}

    # Iterate over features
    for i, feature in enumerate(features):
        # Extract SHAP values for this feature across all samples
        feature_shap_values = shap_values[:, i]

        # Calculate statistics
        mean_shap = float(np.mean(np.abs(feature_shap_values)))
        median_shap = float(np.median(feature_shap_values))
        shap_25th = float(np.percentile(feature_shap_values, 25))
        shap_75th = float(np.percentile(feature_shap_values, 75))

        # Bin the SHAP values
        hist, bin_edges = np.histogram(feature_shap_values, bins=num_bins)
        bins = [
            {
                "bin_range": f"[{float(bin_edges[j]):.2f}, {float(bin_edges[j+1]):.2f}]",
                "count": int(hist[j])
            }
            for j in range(len(hist))
        ]

        # Add detailed data for the feature
        data[feature] = {
            "mean_shap_value": mean_shap,
            "median_shap_value": median_shap,
            "shap_25th_percentile": shap_25th,
            "shap_75th_percentile": shap_75th,
            "binned_shap_values": bins
        }

    # Add feature ranking based on mean SHAP values
    sorted_features = sorted(data.items(), key=lambda x: x[1]["mean_shap_value"], reverse=True)
    ranked_data = {feature: stats for rank, (feature, stats) in enumerate(sorted_features, start=1)}

    # Convert the dictionary to a JSON string
    json_data = json.dumps(ranked_data, indent=4)
    return json_data

def load_shap_data(file_path):
    """
    Load SHAP data from a text file using LangChain's TextLoader.
    Assumes the file contains valid JSON data.
    Handles errors if the file is missing or data is invalid.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found. Please provide a valid file path.")
    
    loader = TextLoader(file_path)
    try:
        documents = loader.load()
        shap_data = json.loads(documents[0].page_content)
        if not shap_data:
            raise ValueError("Error: The file contains no SHAP data.")
        return shap_data
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to parse JSON data from the file. Ensure the file contains valid JSON.")

def chat_with_gpt(prompt, llm_chain, shap_data):
    """
    Chat function that integrates the SHAP data into the user's prompt.
    Handles cases where the SHAP data is empty.
    """
    if not shap_data:
        return "No SHAP data is available. Please provide valid SHAP data to continue."
    
    full_prompt = f"""
    You are an AI assistant specialized in analyzing SHAP (SHapley Additive exPlanations) values and true causal effects from a dataset. Your goal is to:
    1. Analyze feature importance based on SHAP values and their distributions.
    2. Provide simple, actionable insights tailored to the user's question or context.
    3. Summarize findings with a concise, prioritized action plan.
    
    You should aim to:
    - Use plain, accessible language when explaining SHAP values and trends.
    - Avoid unnecessary technical detail; focus on the practical implications of the data.
    - Ensure all recommendations are immediately understandable and actionable.

    For every response:
    1. **Introduction:** Begin with an overview of the dataset and how it relates to the user's query.
    2. **Feature Importance Analysis:**
       - Rank features by mean SHAP values.
       - Explain each feature’s significance and SHAP value distribution in simple terms.
    3. **Data-Driven Recommendations:**
       - Provide actionable insights tied directly to SHAP data.
    4. **Summary:** Prioritize the most impactful actions in a concise conclusion.

    Key Considerations:
    - Simplify SHAP value explanations and relate them to real-world outcomes.
    - Use SHAP distributions (bins and ranges) to support actionable advice.
    - Always tie recommendations back to the data provided.
    - Avoid technical jargon; focus on practical, measurable steps.
    
    Here is the data for reference:
    {json.dumps(shap_data, indent=2)}

    User's question: {prompt}
    """
    response = llm_chain.run({"user_prompt": full_prompt})
    return response.strip()

def initialize_chain():
    """
    Initialize the LLM chain with the GPT model and prompt template.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise EnvironmentError("API key is not set in environment variables.")
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, openai_api_key=openai_api_key)
    template = "User: {user_prompt}\nAssistant:"
    prompt_template = PromptTemplate(input_variables=["user_prompt"], template=template)
    return LLMChain(llm=llm, prompt=prompt_template)


def start_chatbot(shap_file_path):
    """
    Main function to run the chatbot with SHAP data loaded from the specified file.
    Includes error handling for file and data issues.
    """
    try:
        shap_data = load_shap_data(shap_file_path)
    except (FileNotFoundError, ValueError) as e:
        print(f"Chatbot: {e}")
        return

    llm_chain = initialize_chain()
    
    print("Chatbot: I have processed the SHAP data! Please ask any question pertaining to the data!\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Chatbot: Goodbye!")
            break
        
        elif user_input.lower() == "new chat":
            llm_chain = initialize_chain()
            print("\nChatbot: Starting a new chat session...\n")
            continue
        
        try:
            response = chat_with_gpt(user_input, llm_chain, shap_data)
        except Exception as e:
            response = f"An error occurred while processing your request: {e}"
        
        print("\nChatbot:\n", response, "\n")

def load_shap_data(file_path):
    """
    Load SHAP data from a text file using LangChain's TextLoader.
    Assumes the file contains valid JSON data.
    Handles errors if the file is missing or data is invalid.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The file '{file_path}' was not found. Please provide a valid file path.")
    
    loader = TextLoader(file_path)
    try:
        documents = loader.load()
        shap_data = json.loads(documents[0].page_content)
        if not shap_data:
            raise ValueError("Error: The file contains no SHAP data.")
        return shap_data
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to parse JSON data from the file. Ensure the file contains valid JSON.")

def chat_with_prompt_engineering(prompt, llm_chain, shap_data):
    """
    Chat function for the prompt engineering chatbot that integrates SHAP data.
    Refines the user's input prompt and provides context from the SHAP data.
    """
    if not shap_data:
        return "No SHAP data is available. Please provide valid SHAP data to continue."
    
    refined_prompt = f"""
    You are an AI assistant specializing in prompt engineering with access to SHAP (SHapley Additive exPlanations) data. 
    Your job is to:
    - Analyze and refine the user's input prompt for clarity, specificity, and usefulness.
    - Use the SHAP data provided to add meaningful context to your suggestions.
    - Optimize the prompt to ensure it aligns with actionable goals.

    SHAP Data for Reference:
    {json.dumps(shap_data, indent=2)}

    User's input prompt: {prompt}

    Assistant:
    1. **Final Optimized Prompt:** [Provide a fully optimized version of the prompt.]
    """
    response = llm_chain.run({"user_prompt": refined_prompt})
    return response.strip()

def initialize_prompt_chain():
    """
    Initialize the LLM chain for the prompt engineering chatbot.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise EnvironmentError("API key is not set in environment variables.")
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, openai_api_key=openai_api_key)
    template = "{user_prompt}"
    prompt_template = PromptTemplate(input_variables=["user_prompt"], template=template)
    return LLMChain(llm=llm, prompt=prompt_template)

def prompt_engineer(shap_file_path):
    """
    Main function to run the interactive prompt engineering chatbot with SHAP data.
    """
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    try:
        shap_data = load_shap_data(shap_file_path)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return

    try:
        llm_chain = initialize_prompt_chain()
    except EnvironmentError as e:
        print(f"Error: {e}")
        return

    print("Prompt Engineering Chatbot: Ready to refine your prompts with SHAP data! Type 'quit' to exit.\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Chatbot: Goodbye!")
            break
        
        elif user_input.lower() == "new chat":
            try:
                llm_chain = initialize_prompt_chain()
                print("\nChatbot: Starting a new chat session...\n")
            except Exception as e:
                print(f"Chatbot: Error initializing new session: {e}")
            continue
        
        try:
            response = chat_with_prompt_engineering(user_input, llm_chain, shap_data)
        except Exception as e:
            response = f"An error occurred while processing your request: {e}"
        
        print("\nChatbot:\n", response, "\n")