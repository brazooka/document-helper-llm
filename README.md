## 🏗️ Project Structure

- `my_main.py`: Main Streamlit application file
- `my_ingestion.py`: Script for ingesting Quran text into Pinecone vector store
- `backend/my_core.py`: Core functionality for LangChain integration
- `.env`: Environment variables configuration

## 💻 Usage

1. Start the application using `streamlit run my_main.py`
2. The application will open in your default web browser
3. Use the sidebar to customize your user profile
4. Enter your questions about the Quran in the chat interface
5. View answers with source citations and chat history

## 🔍 How It Works

1. **Data Ingestion** (`my_ingestion.py`):
   - Loads the Quran text from a file
   - Splits text into chunks using RecursiveCharacterTextSplitter
   - Embeds chunks using OpenAI's text-embedding-3-small model
   - Stores vectors in Pinecone

2. **Backend Processing** (`my_core.py`):
   - Uses LangChain's retrieval chain for question answering
   - Implements history-aware retrieval for context-aware responses
   - Integrates with OpenAI's ChatGPT for generating responses

3. **Frontend Interface** (`my_main.py`):
   - Provides a Streamlit-based user interface
   - Manages user profiles and chat history
   - Displays responses with source citations

## ⚠️ Important Notes

- Ensure your OpenAI API key has sufficient credits
- The application requires an active internet connection
- The Quran text file should be placed at the specified path in `my_ingestion.py`
- Make sure to have sufficient Pinecone vector store capacity

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

[Add your license information here]
