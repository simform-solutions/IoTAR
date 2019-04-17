using System.Collections;
using System.Collections.Generic;
using UnityEngine;
//using System.IO.Ports;
using UnityEngine.UI;

public class Move : MonoBehaviour
{
    string temp;
    string hum;
    public string jsonRate;
    WWW www;
    public Text temperature;
    public Text humidity;


    void Start()
    {
   
    }

    //Obtain temperature & humidty value from the thingspeak Cloud using JSON
    IEnumerator WaitForRequest(WWW www)
    {
        yield return www;
        // check for errors
        if (www.error == null)
        {
            string work = www.text;

            RootObject fields = JsonUtility.FromJson<RootObject>(work);
            //get temperature value from json
            jsonRate = fields.feeds[0].field1;
            temp = jsonRate.Substring(0, 2);
            //get humidity value from json
            jsonRate = fields.feeds[0].field2;
            hum = jsonRate.Substring(0, 2);
            //Debug to console
            Debug.Log(temp);
            Debug.Log(hum);
         
        }
        else { }
    }

    //Class defined to obtain the Cloud Variable Name and Result
    [System.Serializable]
    public class _Particle
    {                        
        public string userId;
        public string id;
        public string title;
        public string completed;
    }
    [System.Serializable]
    public class Channel
    {
        public int id;
        public string name;
        public string latitude;
        public string longitude;
        public string field1;
        public string created;
        public string update;
        public int last_entry_id;
    }
    [System.Serializable]
    public class Feed
    {
        public string created_at;
        public int entry_id;
        public string field1;
        public string field2;
    }
    [System.Serializable]
    public class RootObject
    {
        public Channel channel;
        public List<Feed> feeds;
    }


    void Update()
    {
        //thingspeak cloud cURL
        string url = "https://api.thingspeak.com/channels/444510/feeds.json?results=2";
        www = new WWW(url);
        StartCoroutine(WaitForRequest(www));
        //set temperature & humidty value on model 
        temperature.text = temp;
        humidity.text = hum;

    }
}