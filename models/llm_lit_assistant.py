import time
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup


def llm_chat(client, model, system_prompt, user_prompt, retry=1, **kwargs):
    for attempt in range(retry, 0, -1):

        try:
            response = client.chat.completions.create(
                model=model,
                temperature=0,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                **kwargs,
            )
            answer_str = response.choices[0].message.content
            print(f"LLM answer: {answer_str}")

            if not answer_str.lower().startswith("n/a"):
                break

        except Exception as err:
            answer_str = f"ERROR: {err}"
            print(answer_str)
            if attempt != 1:
                print(f"{attempt - 1} attempts left. Retry in 60 seconds.")
                time.sleep(60)

    return answer_str


def extract_synthesis_paragraph(folder_path, client, model, retry=5):
    """Extract polymerization reaction related paragraph from each of the papers."""

    print(f"Folder: {folder_path}")

    file_names = []
    response_msgs = []

    for file in Path(folder_path).glob('*.txt'):

        print(f"Extracting paragraph from paper: {file.name}")

        file_names.append(file.name)
        file_contents = open(file, 'r').read()

        system_prompt = (
            "Answer the question as truthfully as possible using the "
            "provided context."
        )

        user_prompt = (
            "This is a research paper related to polymers synthesis: "
            f"{file_contents}."
            "Your task is read the whole text and identify all the "
            "paragraphs that describe the synthetic methods. Your output "
            "should be strictly only these paragraphs without modifying "
            "their context and without adding any other wording."
        )

        answer_str = llm_chat(client, model, system_prompt, user_prompt, retry)
        response_msgs.append(answer_str)

    return pd.DataFrame(
        {'file_name': file_names, 'synthesis_paragraphs': response_msgs}
    )


def extract_chemical_elements(df, client, model, retry=3):
    """Extract all chemical elements from the synthesis paragraph."""

    newkey = 'chemicals'

    for ix in df.index:

        print(f"Extracting chemicals from paper: {df.loc[ix, 'file_name']}")

        paragraph = df.loc[ix, 'synthesis_paragraphs']
        if paragraph.startswith('ERROR: '):
            df.loc[ix, newkey] = None
            continue

        system_prompt = (
            "You are a highly intelligent and accurate polymers domain "
            "expert. Answer the question as truthfully as possible using "
            "the provided context. If you cannot identify the entities "
            'return "N/A".'
        )

        user_prompt = (
            "This is a paragraph related to polymers synthesis.\n\n"
            f"Context:\n{paragraph}"
            "Your task is to identify all the chemical elements used in the "
            "polymerization reaction only. Then generate an HTML version of "
            "the input text, marking up specific entities related to "
            "chemical elements. The specific elements that need to be "
            "identified are the following: base, solvents, ligands, and "
            "catalysts. Use HTML <span> tags to highlight these entities. "
            "Each <span> should have a class attribute indicating the type "
            "of the entity."
        )

        answer_str = llm_chat(client, model, system_prompt, user_prompt, retry)
        df.loc[ix, newkey] = answer_str

    return df[['file_name', newkey]]


def extract_chemical_statistics(df, client, model, retry=3):
    """Extract statistics of chemicals."""

    list_chemicals = [get_elements(s) for s in df['chemicals']]
    list_chemicals = [s for sublist in list_chemicals for s in sublist]

    system_prompt = (
        "You are a highly intelligent and accurate polymers domain expert. "
        "Answer the question as truthfully as possible using the provided "
        "context and save the results in a json file."
    )

    user_prompt = (
        "This is a list with all the chemical elemenents used in a "
        "polymerization reaction."
        f"\n\nContext:\n{list_chemicals}\n"
        "Your task is to count all the instances and return"
        "a dictionary with the main general categories (base, solvents, "
        "ligands, catalysts) as keys, elements that belong to each category "
        "as subkeys and the number of instances as values on the subkeys. "
        "Some elements that are similar should be considered as the same "
        "element, e.g., THF and dry THF are the same elemement and should "
        "belong to the same category. Another example FeCl3 and iron (III) "
        "cloride is the same element and should belong to the same category. "
        "Also Pd(OAc)2 and palladium (II) acetate. Also remove from the list "
        "any toxic solvent such as cloroform, hexane."
    )

    response_msgs = []
    answer_str = llm_chat(
        client,
        model,
        system_prompt,
        user_prompt,
        retry,
        response_format={"type": "json_object"},
    )

    response_msgs.append(answer_str)

    return response_msgs


def get_elements(html_text):

    # Parse the HTML
    soup = BeautifulSoup(html_text, 'html.parser')

    # Classes of interest
    # classes = ["solvents", "ligands", "catalysts", "base"]

    # Initialize an empty list to store highlighted words
    highlighted_words = []

    # Extract words for each class and add to the list
    # for class_name in classes:
    for span in soup.find_all('span'):  # , class_=class_name):
        highlighted_words.append(span.text)

    # Display the list of highlighted words
    return highlighted_words
