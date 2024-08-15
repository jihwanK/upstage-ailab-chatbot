import time

from dotenv import load_dotenv
load_dotenv()

import argparse
import math
import multiprocessing
from tqdm import tqdm

import openai
from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter

def parse_kor_result(data):
    try:
        script = data["text"]["data"]["script"]
        results = [
            f"{scr['role']}: {scr['dialogue']}\n" for scr in script if "role" in scr
        ]
        pooh_inc = any(scr["role"].lower() == "pooh" for scr in script if "role" in scr)
    except:
        return "", False
    return "".join(results), pooh_inc


def extract_scripts(documents, schema):
    llm = ChatOpenAI(model_name="chatgpt-4o-latest", temperature=0)

    kor_chain = create_extraction_chain(llm, schema)

    doc_script = []
    pbar = tqdm(total=len(documents))

    idx = 0
    while idx < len(documents):
        try:
            doc = documents[idx]
            script = kor_chain.invoke(doc.page_content)
            script_parsed, holmes_inc = parse_kor_result(script)
            if holmes_inc:
                doc_script.append(script_parsed)
            idx += 1
            pbar.update(1)
        except Exception as e:
            print(e)
            time.sleep(60)

    return doc_script

def get_template():
    example_text = """
        Then they all talked about something else, until it was time for Pooh
        and Piglet to go home together. At first as they stumped along the path
        which edged the Hundred Acre Wood, they didn't say much to each other;
        but when they came to the stream and had helped each other across the
        stepping stones, and were able to walk side by side again over the
        heather, they began to talk in a friendly way about this and that, and
        Piglet said, "If you see what I mean, Pooh," and Pooh said, "It's just
        what I think myself, Piglet," and Piglet said, "But, on the other hand,
        Pooh, we must remember," and Pooh said, "Quite true, Piglet, although I
        had forgotten it for the moment." And then, just as they came to the Six
        Pine Trees, Pooh looked round to see that nobody else was listening, and
        said in a very solemn voice:

        "Piglet, I have decided something."

        "What have you decided, Pooh?"

        "I have decided to catch a Heffalump."

        Pooh nodded his head several times as he said this, and waited for
        Piglet to say "How?" or "Pooh, you couldn't!" or something helpful of
        that sort, but Piglet said nothing. The fact was Piglet was wishing that
        _he_ had thought about it first.
    """

    result = [
        {"role": "Piglet", "dialogue": "If you see what I mean, Pooh"},
        {"role": "Pooh", "dialogue": "It's just what I think myself, Piglet"},
        {"role": "Piglet", "dialogue": "But, on the other hand, Pooh, we must remember"},
        {"role": "Pooh", "dialogue": "Quite true, Piglet, although I had forgotten it for the moment."},
        {"role": "Pooh:", "dialogue": "Piglet, I have decided something."},
        {"role": "Piglet:", "dialogue": "What have you decided, Pooh?"},
        {"role": "Pooh", "dialogue": "I have decided to catch a Heffalump."},
    ]

    schema = Object(
        id="script",
        description="Extract dialogue from given piece of the novel 'Winnie-the-pooh', ignore the non-dialogue parts. When analyzing the document, make the most of your knowledge about the Sherlock Holmes novels you know. When the speaker is not clear, infer from the character's personality, occupation, and way of speaking.",
        attributes=[
            Text(
                id="role",
                description="The character who is speaking, use context to predict the role",
            ),
            Text(
                id="dialogue",
                description="The dialogue spoken by the characters in the context",
            )
        ],
        examples=[
            (example_text, result)
        ],
        many=True,
    )

    return schema

def get_new_template():
    prompt_template = """
        This is a description of Pooh in this novel.
        In the Milne books, Pooh is naive and slow-witted, but he is also friendly, thoughtful, and steadfast. Although he and his friends agree that he is -a bear of very little brain-, Pooh is occasionally acknowledged to have a clever idea, usually driven by common sense. These include riding in Christopher Robin's umbrella to rescue Piglet from a flood, discovering -the North Pole- by picking it up to help fish Roo out of the river, inventing the game of Poohsticks, and getting Eeyore out of the river by dropping a large rock on one side of him to wash him towards the bank.

        Pooh at Owl's house; illustration by E. H. Shepard
        Pooh is also a talented poet and the stories are frequently punctuated by his poems and -hums-. Although he is humble about his slow-wittedness, he is comfortable with his creative gifts. When Owl's house blows down in a windstorm, trapping Pooh, Piglet and Owl inside, Pooh encourages Piglet (the only one small enough to do so) to escape and rescue them all by promising that -a respectful Pooh song- will be written about Piglet's feat. Later, Pooh muses about the creative process as he composes the song.

        Pooh and a honey (-hunny-) pot, E. H. Shepard illustration from Winnie-the-Pooh (1926)
        Pooh is very fond of food, particularly honey (which he spells -hunny-), but also condensed milk and other items. When he visits friends, his desire to be offered a snack is in conflict with the impoliteness of asking too directly. Though intent on giving Eeyore a pot of honey for his birthday, Pooh could not resist eating it on his way to deliver the present and so instead gives Eeyore -a useful pot to put things in-. When he and Piglet are lost in the forest during Rabbit's attempt to -unbounce- Tigger, Pooh finds his way home by following the -call- of the honeypots from his house. Pooh makes it a habit to have -a little something- around 11:00 in the morning. As the clock in his house -stopped at five minutes to eleven some weeks ago-, any time can be Pooh's snack time.
        Pooh is very social. After Christopher Robin, his closest friend is Piglet, and he most often chooses to spend his time with one or both of them. But he also habitually visits the other animals, often looking for a snack or an audience for his poetry as much as for companionship. His kind-heartedness means he goes out of his way to be friendly to Eeyore, visiting him and bringing him a birthday present and building him a house, despite receiving mostly disdain from Eeyore in return. Devan Coggan of Entertainment Weekly saw a similarity between Pooh and Paddington Bear, two -extremely polite British bears without pants-, adding that -both bears share a philosophy of kindness and integrity-.

        novel line:
        {dialogues}

        Dialogue including the speaker:
    """


def main(num_process):
    loader = DirectoryLoader('./dataset', glob="*", show_progress=True)
    docs = loader.load()

    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=2048,
        chunk_overlap=256,
        length_function=len,
        is_separator_regex=False,
    )
    documents = text_splitter.split_documents(docs)
    num_docs = len(documents)

    schema = get_template()

    window = math.ceil(num_docs / (num_process * 10)) * 10
    inputs = [
        (documents[idx : idx + window], schema) for idx in range(0, num_docs, window)
    ]

    pool = multiprocessing.Pool(processes=num_process)
    result = pool.starmap(extract_scripts, inputs)
    result = sum(result, [])

    with open("./dataset/pooh_script.txt", "w") as f:
        f.write("###\n".join(result))

    pool.close()
    pool.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract and process scripts from documents."
    )
    parser.add_argument(
        "--process", type=int, default=8, help="Number of processes to use"
    )

    args = parser.parse_args()
    main(args.process)
