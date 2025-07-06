# Advertisement Monitoring System (AMS)

## Overview
The Advertisement Monitoring System is a sophisticated PyQt5-based desktop application that uses computer vision and deep learning to detect and monitor advertisements in video content. The system can analyze both live broadcasts and archived video files to identify when specific advertisements are played.

## Features

### Core Functionality
- **Feed Advertisement**: Upload and process advertisement videos to create feature databases
- **Monitor Advertisement**: Real-time monitoring of live broadcasts or archived videos
- **History Tracking**: View historical monitoring reports with timestamps
- **Multi-Channel Support**: Monitor multiple live broadcast channels

### Technical Features
- Deep learning-based feature extraction using VGG16 CNN model
- Real-time video processing and frame analysis
- Euclidean distance matching for advertisement detection
- Multi-threaded processing for smooth UI experience
- Automatic thumbnail generation for advertisements

## System Requirements

### Hardware Requirements
- Minimum 4GB RAM (8GB recommended)
- GPU support recommended for faster processing
- Stable internet connection for live broadcast monitoring

### Software Requirements
- Python 3.7+
- Operating System: Windows 10+ (primarily tested)
- Required Python packages (see requirements.txt)

## Installation

1. **Clone or download the project files**
2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Verify directory structure**:
   ```
   AMS/
   ├── main.py
   ├── cleaning2.py
   ├── images/
   ├── ad_thumbs/
   ├── history/
   └── Datasets/
   ```

## Usage

### Starting the Application
```bash
python cleaning2.py
```

### Adding Advertisements
1. Click "Feed Ad" from the main menu
2. Browse and select your advertisement video file (.mp4)
3. Wait for processing to complete
4. The advertisement will appear in the gallery

### Monitoring Advertisements
1. Click "Monitor Ad" from the main menu
2. Select the advertisement you want to monitor
3. Choose monitoring source:
   - **Live Broadcast**: Select from available channels
   - **Local Video**: Browse and select archived video file
4. View real-time monitoring results and reports

### Viewing History
1. Click "History" from the main menu
2. Select a date from the calendar
3. View detailed monitoring reports for that date

## Technical Architecture

### Main Components

#### 1. GUI Layer (`cleaning2.py`)
- **Main Application**: PyQt5-based desktop interface
- **Tab Management**: Multiple tabs for different functionalities
- **Custom Widgets**: Specialized buttons, video players, and layouts

#### 2. Core Processing (`main.py`)
- **Feature Extraction**: VGG16-based CNN for video frame analysis
- **Advertisement Detection**: Euclidean distance matching algorithm
- **Video Processing**: Frame extraction and real-time analysis

### Key Classes

#### GUI Classes
- `Main`: Main application window and tab management
- `MainMenu`: Welcome screen and navigation
- `FeedAd`: Advertisement upload and processing interface
- `MonitorAd`: Real-time monitoring interface
- `History`: Historical data viewer
- `VideoPlayer`: Custom video display widget

#### Processing Classes
- `Thread`: Video frame processing thread
- `ThreadCounter`: Monitoring time counter
- Feature extraction and matching functions

## Configuration

### Supported Video Formats
- MP4 (recommended)
- Other formats supported by OpenCV

### Live Broadcast Channels
- GEO News
- Samaa News
- BOL News
- ARY News

### Detection Parameters
- **Similarity Threshold**: 1.5 (Euclidean distance)
- **Frame Rate**: 1 frame per second analysis
- **Feature Vector Size**: 4096 dimensions

## File Structure

```
AMS/
├── main.py                 # Core processing and ML functions
├── cleaning2.py           # GUI application and user interface
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── images/               # UI images and logos
│   ├── logo.ico
│   ├── back.jpg
│   ├── geo_logo.png
│   ├── samaa_logo.png
│   ├── bol_logo.png
│   └── ary_logo.png
├── ad_thumbs/            # Advertisement thumbnails (auto-generated)
├── history/              # Historical monitoring reports
│   └── DD-MM-YYYY/       # Daily report folders
├── Datasets/             # Processing datasets (auto-generated)
│   ├── Ad frames/
│   ├── Live Frames/
│   └── Archive Frames/
└── MODELX                # Trained VGG16 model (auto-generated)
```

## Troubleshooting

### Common Issues

1. **"Model not found" Error**
   - Ensure all dependencies are installed
   - Run the application once to generate the model

2. **Video Processing Errors**
   - Check video format compatibility
   - Verify internet connection for live broadcasts

3. **Memory Issues**
   - Close other applications
   - Reduce video resolution if possible

### Performance Optimization
- Use GPU acceleration if available
- Close unnecessary applications during monitoring
- Ensure stable internet connection for live broadcasts

## Technical Details

### Machine Learning Model
- **Base Model**: VGG16 (pre-trained on ImageNet)
- **Feature Extraction**: 4096-dimensional vectors
- **Matching Algorithm**: Euclidean distance with threshold 1.5
- **Frame Processing**: 1 FPS for real-time analysis

### Data Flow
1. Video input → Frame extraction
2. Frame preprocessing → Feature extraction
3. Feature comparison → Match detection
4. Result logging → Report generation

## Development Information

### Authors
- Muhammad Furqan Javed Afridi (01-134191-082)
- Hassan Raza Khan Tareen (01-134191-081)

### Contact
- furqanjavedafridi@gmail.com
- hrkhan390@gmail.com

### Development Date
October 1, 2022

### Class
BS CS 8B

## License
This project is developed as an academic project. Please respect the authors' intellectual property rights.

## Future Enhancements
- Support for additional video formats
- Enhanced GUI with more customization options
- Cloud-based processing capabilities
- Mobile application support
- Advanced analytics and reporting features

## Disclaimer
This system is designed for educational and research purposes. Users are responsible for complying with applicable laws and regulations regarding video content monitoring and analysis.
