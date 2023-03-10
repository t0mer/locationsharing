# locationsharing
A Docker container to retrieve coordinates from a google account that has been shared with locations of other accounts and add it as a device tracker to Home Assistant. The container publishes the info using mqtt auto discovery without the need for special configuration on the Home Assistant side.

## Install
Use the following docker-compose file for the container installation:

```yaml
version: "3.6"
services:
  locationsharing:
    image: techblog/locationsharing
    container_name: locationsharing
    restart: always
    environment:
      - EMAIL_ADDRESS= #Google account email
      - COOKIES_FILE_NAME= #Cookies file name (File name without path)
      - MQTT_HOST= #MQTT Host address
      - MQTT_PORT= #MQTT Port,Default is 1883
      - MQTT_USERNAME= #MQTT Username
      - MQTT_PASSWORD= #MQTT Password
      - UPDATE_INTERVAL=1 #In minutes
    volumes:
      - ./locationsharing/cookies:/app/cookies
```

### *cookies.txt* file
* You must sign out and manually sign into your Google account. Then browse to google.com/maps and extract from your "google.com" cookies and save it as cookies.txt
* Checkout [this chrome extension](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid/related?hl=en) to help export such file very easily.
* Once cookies.txt is created, if the Google account is signed out, it will invalidate the cookies.
* Create the **./locationsharing/cookies** volume and place the cookies file inside it. 
* Next, set all the Environment variables and run docker-compose up -d to set up the container.

The container will run two scripts:
1. The location-sharing script that creates the device_tracker and updates the information.
2. The second script is responsible for refreshing the cookies and keeping is up to date.
