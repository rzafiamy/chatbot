class Config:
    WINDOW_SIZE = "600x800" # Width x Height
    SCRIPT_PATH = "/home/cook/Documents/Dev/llama.cpp/main" # Path to the compiled Llama.cpp script
    # MODEL_PATH = "/home/cook/Documents/Dev/llama.cpp/models/Phi-3-mini-4k-instruct-q4.gguf" # Path to the model file
    MODEL_PATH = "/home/cook/Documents/Dev/llama.cpp/models/Llama-3-8B-Instruct-32k-v0.1.Q3_K_M.gguf" # Path to the model file
    
    NGL = 32 # Number of layer to offload to the GPU
    BATCH = 128 # Batch size , default : 2048
    N = 300 # Number of tokens to generate, default : 128
    C = 4000 # number of context tokens,  default : 512
    REPEAT_PENALTY = 1.5 # Repeat penalty for the model, default : 1.1
    TEMPERATURE = 0.6 # Temperature for the model, default : 0.8

    # User and bot message styling
    USER_BG = "#DFF0D8" # Background of user messages
    USER_FG = "#3C763D" # Foreground (text) color of user messages
    BOT_BG = "#D9EDF7" # Background of bot messages
    BOT_FG = "#31708F" # Foreground (text) color of bot messages

    # Font settings
    FONT_FAMILY = "Iosevka" # Font family
    FONT_SIZE = 12 # Font size
    FONT_STYLE_USER = ("Iosevka", 12, "bold") # Font style for user messages
    FONT_STYLE_BOT = ("Iosevka", 12) # Font style for bot messages
