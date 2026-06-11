from groq import Groq
import os

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)


def groq_response(text):

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        print(f"Groq Error: {e}")

        return None


if __name__ == "__main__":

    question = input("Ask Emma: ")

    answer = groq_response(question)

    print("\nAI Response:\n")
    print(answer)