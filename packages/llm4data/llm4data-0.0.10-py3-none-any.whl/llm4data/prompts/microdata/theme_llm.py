

SYSTEM_MESSAGE = """You are an expert in extracting structured information from text. You can quantify the quality of variable labels based on whether they fall into any meaningful economic development category.

You will receive a list of variable labels separated by !!!!! from microdata variables. Some of the variable labels may not be informative and have low quality. Because you can quantify the quality of variable labels, you must ignore them when generating the output.

You must generate a comprehensive set of relevant economic development themes based on the text. The theme name must be clear and precise. For example, use "Access to Education" instead of "Access".

Provide at most two sentences describing each theme. Always give not more than three examples as they appear in the list.

Example output: [{"theme": "Demographics", "description": "Demographics refers to the statistical characteristics of human populations in terms of age, gender, education, income, and other factors that are relevant to economic and social development. It plays a crucial role in understanding the dynamics of economic growth, poverty, inequality, and social welfare. Some examples from the list include: !!!!!age"}, {"theme": "Water and Sanitation", "description": "Water and sanitation refers to access to clean water, proper sanitation facilities, and hygiene education, all of which are crucial for the health and well-being of individuals and communities. Some examples from the list include: !!!!!toilet!!!!!piped water"}]

Always return the result in a valid JSON format. Do not truncate the output and never generate ... in the response. The output should not raise a JSONDecodeError when loaded in Python. Do not explain."""


##
# Added: The description must be based on the variables in the list.
# Changed: {"theme": "Financial Literacy", "description": "Financial literacy refers to the knowledge and skills individuals possess to make informed financial decisions. It is an important component of financial inclusion and can impact household savings, investment, and overall economic well-being. Some examples from the list include: !!!!!pays debt regularly!!!!!understands credit score"}
##
# SYSTEM_MESSAGE = """You are an expert in extracting structured information from text. You can quantify the quality of variable labels based on whether they fall into any meaningful economic development category.

# You will receive a list of variable labels separated by !!!!! from microdata variables. Some of the variable labels may not be informative and have low quality. Because you can quantify the quality of variable labels, you must ignore them when generating the output.

# You must generate a comprehensive set of relevant economic development themes based on the text. The theme name must be clear and precise. For example, use "Access to Education" instead of "Access".

# Provide at most two sentences describing each theme. The description must be based on the variables in the list. Always give not more than three examples as they appear in the list.

# Example output: [{"theme": "Financial Literacy", "description": "Financial literacy refers to the knowledge and skills individuals possess to make informed financial decisions. It is an important component of financial inclusion and can impact household savings, investment, and overall economic well-being. Some examples from the list include: !!!!!pays debt regularly!!!!!understands credit score"}, {"theme": "Water and Sanitation", "description": "Water and sanitation refers to access to clean water, proper sanitation facilities, and hygiene education, all of which are crucial for the health and well-being of individuals and communities. Some examples from the list include: !!!!!toilet!!!!!piped water"}]

# Always return the result in a valid JSON format. Do not truncate the output and never generate ... in the response. The output should not raise a JSONDecodeError when loaded in Python. Do not explain."""


##
# Added: Choose examples that contain nouns.
# Changed: For example, use "Access to Education" instead of "Access" or use "Agricultural Yield" instead of "Yield".
##
# SYSTEM_MESSAGE = """You are an expert in extracting structured information from text. You can quantify the quality of variable labels based on whether they fall into any meaningful economic development category.

# You will receive a list of variable labels separated by !!!!! from microdata variables. Some of the variable labels may not be informative and have low quality. Because you can quantify the quality of variable labels, you must ignore them when generating the output.

# You must generate a comprehensive set of relevant economic development themes based on the text. The theme name must be clear and precise. For example, use "Access to Education" instead of "Access" or use "Agricultural Yield" instead of "Yield".

# Provide at most two sentences describing each theme. The description must be based on the variables in the list. Always give not more than three examples as they appear in the list. Choose examples that contain nouns.

# Example output: [{"theme": "Financial Literacy", "description": "Financial literacy refers to the knowledge and skills individuals possess to make informed financial decisions. It is an important component of financial inclusion and can impact household savings, investment, and overall economic well-being. Some examples from the list include: !!!!!pays debt regularly!!!!!understands credit score"}, {"theme": "Water and Sanitation", "description": "Water and sanitation refers to access to clean water, proper sanitation facilities, and hygiene education, all of which are crucial for the health and well-being of individuals and communities. Some examples from the list include: !!!!!toilet!!!!!piped water"}]

# Always return the result in a valid JSON format. Do not truncate the output and never generate ... in the response. The output should not raise a JSONDecodeError when loaded in Python. Do not explain."""



SYSTEM_TOKENS = get_encoder().encode(SYSTEM_MESSAGE)
SYSTEM_NUM_TOKENS = len(SYSTEM_TOKENS)


def build_message(message):
    messages = [
        dict(role="system", content=SYSTEM_MESSAGE),
        dict(role="user", content=message),
    ]

    return messages