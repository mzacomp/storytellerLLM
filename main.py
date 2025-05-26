#Address this in the beginning for submission
"""
Before submitting the assignment, describe here in a few sentences what you would have built next if you spent 2 more hours on this project:

I would have: 

- Adapted the categorization strategy to be more advanced. I would process the user requests into explicit categories that would have been sent to some sort of backend
database and also enforced that these categorizations would tailor the LLM's response. 
-Incorporated reinforcement learning for the main storyteller LLM to improve itself based on both the judge LLM and user feedback. I laid the 
groundwork for this but I would have developed it further. I would have also considered the possibility of using the RAG framework. 
-Incorporated more fail-safe prompting, meaning if the user requests a story that is inappropriate for the age group how the LLM should address this. 
-Developed the frontend in some way, demonstrate full-stack capabilities
-Considered using Voice AI, which I think this use case would be a suitable for 


"""

#Storyteller LLM (main LLM with GPT 3.5 Turbo)
#Libraries
import openai 
import os 
from dotenv import load_dotenv

#Load OpenAI Key
load_dotenv() 

openai.api_key = os.getenv("OPEN_AI_KEY")


#Prompting 

#StoryTeller LLM Prompt 

story_prompt_template = """
You are a delightful and whimsical storyteller. You produce engaging stories for the consumption of young children aged from 5 years old to 10 years old.
It is critical that these stories are approporiate for children within in this specific age group. 

You must adhere to the user request. If the user request includes specific names (e.g., Max, Anna), you must use these exact names in the story.If the user request includes
explicit mentioning of themes, tone, intended message, story type, and/or structure type, you must incorporate these in the story.


A user made a following request: 
"{user_request}"

You should reason internally about the best theme, tone, message, story type, and structure type.

Then write a ~400-word bedtime story that:
- Matches the inferred theme and tone
- Conveys the intended message
- Has a clear beginning, middle, and end
- Uses vivid and simple language appropriate for ages 5-10
- Ends with a comforting, optimistic sentence


If the user requests a story that is graphic in nature and violent, and would ultimately violate the age-appropriateness of this age group, respond with this: 
"That is outside the bounds of imagination. Happy to help with another story that is more suited for whimsical bedtime stories!" 

Only return the final story. Do not include any step labels, bullet points, or explicit categorization.

"""

#LiteraryJudge LLM Prompt 

judge_template = """


You are a literary expert evaluating children's bedtime stories.

Please review the story below and rate it (1-5) on:
1. Relevance to the request
2. Story structure (beginning, middle, end)
3. Language simplicity (age 5-10)
4. Tone (child-appropriate)
5. Creativity and imagination

Then provide 1-2 suggestions for improving it.

Story:
{story_text}
"""


#Revisor LLM - Based on Judge Feedback and User Feedback 

judge_improvement_prompt = """ 
   
You are a children's story editor.

Here is the original story:
{story_text}

Here is the judge's feedback: "{judge_feedback}"

Please revise the story to address the judge's suggestions, while maintaining its tone and age-appropriateness.
Keep the revised version about 400 words and end with a comforting  sentence.
"""


user_feedback_prompt =  """

You are a children's story editor.

Here is the original story:
{story_text}

The user provided this feedback: "{user_feedback}"

Please revise the story to reflect this feedback while keeping it appropriate for children aged 5-10.
Maintain the tone and structure, and keep the length around 400 words.

"""
   
judge_user_feedback_prompt = """
You are a literary evaluator reviewing how well a story was revised based on user feedback.

Here is the user's feedback:
"{user_feedback}"

Here is the final revised story:
{revised_story}

Evaluate how well the story incorporates the user's feedback. Rate from 1-5 and explain your reasoning in 2-3 sentences.

"""


# Model Calling 


def call_story_model(user_request:str, max_tokens=3000, temperature=0.1) -> str:
    prompt = story_prompt_template.format(user_request=user_request)
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}], #
        stream=False,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message["content"]  # type: ignore

def call_judge_model(story_text: str, max_tokens=3000, temperature=0.1) -> str:
     prompt = judge_template.format(story_text=story_text)
     resp = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}], #
        stream=False,
        max_tokens=max_tokens,
        temperature=temperature,
    )
     return resp.choices[0].message["content"]  


def call_judge_improvement(story_text:str, judge_feedback:str, max_tokens=3000, temperature=0.1) -> str:
    prompt = judge_improvement_prompt.format(story_text=story_text,judge_feedback=judge_feedback)
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}], #
        stream=False,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message["content"]  # type: ignore


def call_user_improvement(story_text:str, user_feedback:str, max_tokens=3000, temperature=0.1) -> str:
    prompt= user_feedback_prompt.format(story_text=story_text,user_feedback=user_feedback)
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}], #
        stream=False,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message["content"]  # type: ignore


def call_user_feedback_judge(revised_story: str, user_feedback: str, max_tokens=3000, temperature=0.1) -> str:
    prompt= judge_user_feedback_prompt.format(revised_story=revised_story, user_feedback=user_feedback)
    resp = openai.ChatCompletion.create(
       model="gpt-4o",
       messages=[{"role": "user", "content": prompt}], 
       stream=False,
       max_tokens=max_tokens,
       temperature=temperature,
    )
    return resp.choices[0].message["content"]  



#Main Orchestration

def main():
    user_input = input("Hello, I am DreamTales. I am a storyteller LLM to create engaging stories for young children. What story shall we embark on?")
    initial_story = call_story_model(user_input)
    print("\nHere is your Dream Tale:\n")
    print(initial_story)

    judge_feedback = call_judge_model(initial_story)
    print("\n\nExpert Judge Feedback:\n")
    print(judge_feedback)

    judge_improvement_story= call_judge_improvement(initial_story, judge_feedback)
    print("\nHere is the improved story based on expert feedback:\n")
    print(judge_improvement_story.strip())

    user_feedback = input("\nWould you like to request any changes to the story? (Leave blank to skip)\n")
    if user_feedback.strip():
        revised_story = call_user_improvement(judge_improvement_story, user_feedback)
        print("\nHere is the revised story based on your feedback:\n")
        print(revised_story.strip())

        judge_feedback_on_user_request = call_user_feedback_judge(revised_story, user_feedback)
        print("\nExpert Judge's Evaluation of Feedback Incorporation:\n")
        print(judge_feedback_on_user_request.strip())
    else:
        print("\nNo additional changes requested. Sweet dreams!")


if __name__ == "__main__":
    main()
