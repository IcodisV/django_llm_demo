## API Description

The Django LLM Demo API exposes chatbot conversation data simulated between two OpenAI GPT instances.

### Available Endpoints

- **GET `/api/conversations/`**  
  Retrieves all chatbot conversations. Each record contains:  
  - `question`: The prompt asked by ChatGPT A  
  - `answer`: The response from ChatGPT B  
  - `is_vegetarian`: Boolean indicating if the foods mentioned are vegetarian  
  - `timestamp`: When the conversation occurred  

- **GET `/api/vegetarian_conversations/`**  
  Retrieves only conversations flagged as vegetarian, filtering for users whose favorite foods are vegetarian.

### Authentication

- Access to these endpoints is protected with **Basic Authentication**.  
- Use the username and password credentials provided to authenticate your requests.


### Purpose

These endpoints enable retrieving and analyzing chatbot conversation data, supporting features like dietary preference insights and user segmentation.
