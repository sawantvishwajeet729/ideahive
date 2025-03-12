![Logo](https://github.com/sawantvishwajeet729/ideahive/blob/main/artifacts/idea_hive.png)

## Introduction
IdeaHive is a web application that utilizes Reddit's vast conversation data to generate business ideas. By leveraging large language models and natural language processing techniques, IdeaHive provides users with actionable insights and potential solutions to real-world problems.

## Features
* **Reddit Post Analysis**: IdeaHive extracts relevant posts from Reddit based on user-inputted topics.
* **Business Idea Generation**: The application uses large language models to analyze the extracted posts and generate structured business ideas.
* **Customizable LLM Models**: Users can select from a variety of large language models to suit their specific needs.
* **User-Friendly Interface**: IdeaHive features a simple and intuitive interface, making it easy for users to navigate and utilize the application.

## Technical Overview
IdeaHive is built using the following technologies:
* **Streamlit**: A Python library for building web applications.
* **Langchain**: A library for building and integrating large language models.
* **PRAW**: A Python wrapper for the Reddit API.
* **FAISS**: A library for efficient similarity search and clustering.

## Requirements
To run IdeaHive, you will need to install the following dependencies:
* `praw`
* `langchain`
* `langchain_community`
* `langchain_openai`
* `langchain_core`
* `faiss-cpu`
* `langchain_groq`
* `streamlit`

## Setup
1. Clone the repository and navigate to the project directory.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up your Reddit API credentials and OpenAI API key as environment variables.
4. Run the application using `streamlit run front_end.py`.

## Usage
1. Open the link [ideaHive](https://ideahive.streamlit.app/) in your web browser.
2. Select a topic of interest and choose a large language model.
3. Press "Enter" to generate a business idea based on the extracted Reddit posts.

## Contributing
Contributions to IdeaHive are welcome. If you have any suggestions or improvements, please submit a pull request or open an issue.

## License
IdeaHive is licensed under the MIT License. See the LICENSE file for more information.

## Authors

- [@VishwajeetSawant](https://github.com/sawantvishwajeet729)

## Contact
For any questions or feedback, please contact Vishwajeet Sawant at [sawantvishwajeet729@gmail.com](mailto:sawantvishwajeet729@gmail.com).