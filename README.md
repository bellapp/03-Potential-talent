# Job Similarity Search Application 🔍

A powerful Streamlit application that performs intelligent similarity searches on job titles using various AI models including multiple models running in different platforms:  Mistral (Ollama), Groq and HuggingFace.

## 🌟 Features

- **Multiple Model Support**: Choose between local (Ollama), Groq, or HuggingFace models
- **CSV File Processing**: Upload and analyze job titles from CSV files
- **Interactive Interface**: User-friendly Streamlit interface with real-time results
- **Smart Analysis**: AI-powered similarity matching and job title analysis
- **Docker Support**: Easy deployment using Docker containers

## 🚀 Quick Start

### Prerequisites

- Docker Desktop
- Git (optional)

### Installation

1. Clone the repository:

```
git clone https://github.com/bellapp/potential-talents potential-talents
```

1. Start the application:

```
start.bat
```

1. Access the application at: http://localhost:8501

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Models**:
  - Ollama (Local)
  - Groq
  - HuggingFace
- **Data Processing**: Pandas, LangChain
- **Containerization**: Docker

## 📁 Project Structure

```
potential-talents/  ├── app/│   
                        ├── app.py│   
                        └── requirements.txt
                    ├── docker/│   
                        └── Dockerfile.streamlit
                    ├── docker-compose.yml
                    ├── start.bat
                    └── stop.bat
```

## 🔧 Configuration

1. Create a `.env` file with your API keys (optional):

```
GROQ_API_KEY=your_groq_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

1. Configure Docker resources in Docker Desktop settings

## 📊 Usage

1. Start the application using `start.bat`
1. Upload your CSV file containing job titles
1. Enter your search query
1. Select your preferred model
1. View the analysis results

## 📋 CSV Format

Your CSV file should contain job titles with a semicolon (;) delimiter:

```
job_titleSoftware EngineerData ScientistProduct Manager
```

## 🐳 Docker Commands

- Start services: `start.bat`
- Stop services: `stop.bat`
- View logs: `docker-compose logs -f`

## 🤝 Contributing

1. Fork the repository
1. Create your feature branch (`git checkout -b feature/AmazingFeature`)
1. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
1. Push to the branch (`git push origin feature/AmazingFeature`)
1. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Abdelaaziz Bellout - Initial work - [Bellapp](https://github.com/bellapp)

## 🙏 Acknowledgments

- Ollama team for the local model support
- Streamlit team for the amazing framework

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers.

---

Made with ❤️ by [Abdelaaziz Bellout]