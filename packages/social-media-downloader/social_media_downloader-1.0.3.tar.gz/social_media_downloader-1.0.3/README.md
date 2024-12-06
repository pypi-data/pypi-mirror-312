
# **Social Media Downloader**  

**Social Media Downloader** is a powerful, user-friendly tool designed to help you download videos, photos, and audio from popular social media platforms like **YouTube**, **Facebook**, **Instagram**, and **TikTok**. With advanced capabilities like batch downloading, format selection, and integrated update checking, this tool provides a seamless experience for both casual and power users.  

---

## **What's New in v1.0.2**  
- **Batch Download Support**: Easily download multiple media files in one go using a text file with URLs.  
- **Facebook Video Downloads**: Enhanced support for Facebook videos using scraping techniques to retrieve media.  
- **Progress Bar Integration**: Visual progress tracking for all downloads.  
- **Improved Update Checker**: Checks for the latest version and simplifies the update process.  
- **Advanced Logging**: Tracks download history in `download_history.csv` and logs detailed events in `downloader.log`.  

For a complete changelog, see the [WHAT'S NEW](whats_new.txt) file.  

---

## **Features**  
### Core Features  
- **Platform Support**: Download from **YouTube**, **TikTok**, **Instagram**, and **Facebook**.  
- **Flexible Format Selection**: Choose your desired video quality and format or extract audio as MP3.  
- **Batch Downloading**: Add multiple URLs in a text file for simultaneous downloading.  

### Enhanced Functionality  
- **Update Checker**: Stay updated with the latest version using an integrated update mechanism.  
- **Download History**: Automatically logs download attempts, including success/failure status and timestamps.  
- **Error Handling**: Provides detailed error messages for unsupported platforms or invalid URLs.  
- **Built-in Help Menu**: Access a detailed usage guide directly within the program.  
- **Cross-Platform Support**: Works seamlessly on both Windows and Linux systems.  

---

## **Installation**  

### **Windows**  
1. [Download the latest Windows executable](https://github.com/nayandas69/social-media-downloader/releases/latest).  
2. Run the downloaded file (`Downloader_v1.0.3.exe`).  

### **Linux**  
1. [Download the latest Linux release](https://github.com/nayandas69/social-media-downloader/releases/latest).  
2. Extract the downloaded archive:  
   ```bash
   unzip Downloader_v1.0.3_Linux.zip  
   ``` 
   or
   ```bash  
   tar -xzvf Downloader_v1.0.3_Linux.tar.gz  
   ```  
3. Navigate to the extracted folder and run the tool:  
   ```bash  
   ./downloader  
   ```  

---

## **How to Use**  

1. **Launch the Downloader**: Run the program and choose your desired option from the menu.  
2. **Enter URL**: Paste the video or post URL when prompted.  
3. **Choose Format**: For YouTube and TikTok, select your preferred format and quality.  
4. **Enjoy Your Download**: Media files will be saved in the `media` directory.  

### **Available Options**  
1. **Download YouTube/TikTok Video**: Choose your desired quality and download.  
2. **Download Facebook Video**: Download videos from Facebook posts or pages.  
3. **Download Instagram Post**: Save Instagram photos or videos.  
4. **Batch Download**: Provide a text file with multiple URLs for bulk downloading.  
5. **Check for Updates**: Ensure you're using the latest version.  
6. **Help Menu**: Access the built-in help guide.  
7. **Quit**: Exit the program.  

---

## **Examples**  

### **Downloading from YouTube or TikTok**  
1. Choose the **YouTube/TikTok** option from the menu.  
2. Paste the video URL.  
3. Select the desired format or choose "MP3" for audio extraction.  

### **Batch Download**  
1. Create a text file (`urls.txt`) with one URL per line.  
2. Select the **Batch Download** option and provide the path to the file.  

### **Downloading from Instagram**  
1. Copy the Instagram post URL.  
2. Select the **Instagram Download** option and paste the URL when prompted.  

---

## **Requirements**  

### **FFmpeg (Optional)**  
- **FFmpeg** is required for extracting MP3 audio or merging audio and video streams.  

#### Installation Instructions:  
- **Windows**: [Follow this setup guide](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/).  
- **Linux**: Install FFmpeg using the package manager:  
  ```bash  
  sudo apt install ffmpeg  
  ```  

---

## **Download Directory**  
- All media files are saved in the default `media` folder, which is automatically created if it doesn't exist.  
- You can change the default directory in the `config.json` file.  

---

## **Troubleshooting**  
If you encounter any issues:  
- Verify the provided URL is correct and from a supported platform.  
- Ensure **FFmpeg** is installed and correctly configured for MP3 extraction.  
- Check your internet connection.  
- Review the `downloader.log` file for detailed error information.  

For further assistance, contact the author using the details below.  

---

## **License**  
This project is licensed under the **MIT License**. See the [LICENSE](https://github.com/nayandas69/social-media-downloader/blob/main/LICENSE) file for more details.  

---

## **Author**  
- **Name**: Nayan Das  
- **Email**: [Mail Me](mailto:nayanchandradas@hotmail.com)  
- **Website**: [Social Portal](https://socialportal.nayanchandradas.com)  

---

### **Disclaimer**  
> This tool is intended for personal use only. Please respect copyright laws and platform terms of service while using this tool.  

Enjoy downloading your favorite content with **Social Media Downloader v1.0.2**! 🚀  
If you have any feedback, feature suggestions, or bug reports, don’t hesitate to reach out.  

