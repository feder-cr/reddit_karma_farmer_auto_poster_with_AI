import random
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

class GeneratorPostGPT:
    def __init__(self, openai_api_key, model_name="gpt-4o-mini"):
        self.llm = ChatOpenAI(model_name=model_name, openai_api_key=openai_api_key)

    def _preprocess_template_string(self, template_string: str) -> str:
        return template_string

    def determine_best_prompt(self, source_subreddit: str, summary: str, rules: str) -> int:
        prompt = f"""
        Based on the following summary of the top 10 posts from r/{source_subreddit} and the subreddit rules, provide the number corresponding to the best type of post to generate for maximum upvotes:

        1. Extremely clickbait with a very short body.
        2. Clickbait with a medium-length body.
        3. Question-oriented and brief.
        4. Analytical and detailed.
        5. Humorous and short.
        6. Expert opinion and extended.

        Summary:
        {summary}

        Rules:
        {rules}

        Provide the number of the most effective post type.
        """
        prompt_template = ChatPromptTemplate.from_template(prompt)
        chain = prompt_template | self.llm | StrOutputParser()
        response = chain.invoke({
            "source_subreddit": source_subreddit,
            "summary": summary,
            "rules": rules
        })
        try:
            best_prompt_number = int(response)
        except ValueError:
            best_prompt_number = 2

        if random.random() < 0.5:
            best_prompt_number = random.randint(1, 6)
        print(best_prompt_number)
        return best_prompt_number

    def generate_post(self, source_subreddit: str, summary: str, rules: str) -> str:
        best_prompt_number = self.determine_best_prompt(source_subreddit, summary, rules)
        prompt_templates = {
            1: """
            Based on the following summary of the top 10 posts from r/{source_subreddit} and the subreddit rules:

            Summary:
            {summary}

            Rules:
            {rules}

            Create a super-clickbait post designed to get the most upvotes. The post should:

            1. Be really provocative and grab attention right away.
            2. Have a title that makes users click instantly.
            3. Keep the body short and simple (no more than 75 words) to keep people engaged.
            4. Avoid emojis and unnecessary formatting.
            5. Focus on content that’s easy to share and gets people talking.

            Try to use plain, everyday language and make it sound like it was written by a regular user, not AI.

            Response format:

            Title: "(title)"

            Body: "(body)"
            """,
            2: """
            Using the following summary of the top 10 posts from r/{source_subreddit} and the subreddit rules:

            Summary:
            {summary}

            Rules:
            {rules}

            Write a post designed to catch attention and get upvotes. The post should:

            1. Have a super-clickbait title that makes users want to read more.
            2. Have a body that’s interesting and makes people want to comment, with a length between 150 and 250 words.
            3. Avoid links, emojis, and too much punctuation.
            4. Be intriguing and get people thinking.

            Keep the language simple and make it sound like a regular person wrote it, not an AI.

            Response format:

            Title: "(title)"

            Body: "(body)"
            """,
            3: """
            Based on the summary of the top 10 posts from r/{source_subreddit} and the subreddit rules:

            Summary:
            {summary}

            Rules:
            {rules}

            Create a post that gets high engagement by asking thought-provoking questions. The post should:

            1. Have a title that grabs attention and makes people curious.
            2. Have a body of 100 to 150 words that invites discussion and interaction through questions.
            3. Avoid emojis and links, and just focus on the content.
            4. End with a question to get more comments and replies.

            Use plain language and make it sound like it was written by a regular user, not AI.

            Response format:

            Title: "(title)"

            Body: "(body)"
            """,
            4: """
            Analyze the summary of the top 10 posts from r/{source_subreddit} and the subreddit rules to create a post that gets lots of upvotes. The post should:

            1. Have a super-clickbait title that hooks readers immediately.
            2. Provide an in-depth analysis or unique perspective in a body of 250 to 300 words.
            3. Avoid external links, emojis, and extra punctuation.
            4. Encourage readers to engage by offering fresh ideas or strong opinions.

            Use simple language and make it sound like a regular person wrote it, not AI.

            Response format:

            Title: "(title)"

            Body: "(body)"
            """,
            5: """
            Create a funny and super-clickable post based on the summary of the top 10 posts from r/{source_subreddit} and the subreddit rules. Your post should:

            1. Have a clickbait title that promises humor and fun.
            2. Have a body of 150 to 200 words that’s light-hearted and entertaining.
            3. Avoid emojis and links, and just focus on being funny.
            4. Make sure the post is designed to go viral through humor.

            Use plain language and make it sound like it was written by a regular user, not AI.

            Response format:

            Title: "(title)"

            Body: "(body)"
            """,
            6: """
            Based on the summary of the top 10 posts from r/{source_subreddit} and the subreddit rules, create a post that gives expert opinions to get upvotes. Your post should:

            1. Have a clickbait title that draws readers in.
            2. Offer a detailed and expert analysis in a body of 200 to 250 words.
            3. Avoid external links, emojis, and extra punctuation.
            4. Provide information that’s engaging and makes readers want to interact.

            Use plain language and make it sound like it was written by a regular person, not AI.

            Response format:

            Title: "(title)"

            Body: "(body)"
            """
        }
        selected_prompt_template = prompt_templates.get(best_prompt_number)
        prompt = ChatPromptTemplate.from_template(selected_prompt_template)
        chain = prompt | self.llm | StrOutputParser()
        output = chain.invoke({
            "source_subreddit": source_subreddit,
            "summary": summary,
            "rules": rules
        })

        return output
