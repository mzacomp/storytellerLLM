DreamTales - StoryTeller LLM 

by Mahsan Zare


May 26,2025 

![ChatGPT Image May 26, 2025, 12_18_51 PM](https://github.com/user-attachments/assets/9a9acab3-d333-4034-a7ed-ef4351d36562)



For this technical project, I had three LLMs interactions: StoryTellerLLM (main LLM), LiteraryExpertLLM (Judge LLM), RevisorLLM (Feedback LLM to StoryTeller LLM). I incorporated task-oriented prompting for all three LLMs.
The main LLM adheres to the request of the user, the judge LLM assess how well the main LLM completed the task --> provides this feedback to the revisor LLM--> revisor LLM revises the story based on the feedback --> if the user requests changes, the revisor LLM will make these changes --> then the Judge LLM will also judge how well the user feedback was respected. 
I developed a categorization strategy where the storytellerLLM had to create a story based on fulfilling certain categories. I allowed for the user to request changes and provide feedback, and have the Judge LLM judge how well the main LLM incorporated the user's feedback. 

Please refer to the main.py for full code/prompt execution. 

I used my OpenAI key for this technical project.
My IDE was VS Code. 


