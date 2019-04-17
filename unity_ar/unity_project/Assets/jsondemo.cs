using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class jsondemo : MonoBehaviour
{

    public float ForceInput;        //Declare Variables and Strings
    float ParticleVariable;
    string path;
    string Url;
    string jsonRate;
    WWW www;

    public float ForceMode;
    // Start is called before the first frame update
    void Start()
    {
        
    }


    IEnumerator WaitForRequest(WWW www)             //Obtain Variables from the Photon Cloud using JSON
    {
        yield return www;
        // check for errors
        if (www.error == null)
        {
            string work = www.text;

            _Particle fields = JsonUtility.FromJson<_Particle>(work);
            string jsonRate = fields.completed;

           // ParticleVariable = float.Parse(jsonRate);
            Debug.Log(jsonRate);           //Debug to console
            //ForceInput = ParticleVariable;

            fields.title = "my text";
            string newfield = JsonUtility.ToJson(fields);
            Debug.Log(newfield);
        }
        else { }
    }

    [System.Serializable]
    public class _Particle
    {                         //Class defined to obtain the Cloud Variable Name and Result
        public string userId;
        public string id;
        public string title;
        public string completed;
    }


    // Update is called once per frame
    void Update()
    {
        //Insert your cURL here:
        string url = "https://jsonplaceholder.typicode.com/todos/1";
        www = new WWW(url);
        StartCoroutine(WaitForRequest(www));
       // AnalogueSpeedConverter.ShowSpeed(ForceInput, 0, 100); //Send Force reading to analog dial.



    }
}

/*
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
//using System.IO.Ports;
using UnityEngine.UI;

public class Move : MonoBehaviour
{
    //public GameObject Game_Temp;
    public float ForceInput;        //Declare Variables and Strings
    float ParticleVariable;
    string path;
    string Url;
    string temp;
    string hum;
    public string jsonRate;
    WWW www;
    public Text temperature;
    public Text humidity;
    string value;

    //SerialPort sp = new SerialPort("/dev/cu.usbmodem14601", 9600); // set port of your arduino connected to computer


    void Start()
    {
        // sp.Open();
        //sp.ReadTimeout = 1;
    }

    IEnumerator WaitForRequest(WWW www)             //Obtain Variables from the Photon Cloud using JSON
    {
        yield return www;
        // check for errors
        if (www.error == null)
        {
            string work = www.text;

            RootObject fields = JsonUtility.FromJson<RootObject>(work);
            jsonRate = fields.feeds[0].field1;
            temp = jsonRate.Substring(0, 2);
            jsonRate = fields.feeds[0].field2;
            hum = jsonRate.Substring(0, 2);


            // ParticleVariable = float.Parse(jsonRate);
            Debug.Log(temp);           //Debug to console
            Debug.Log(hum);
            //ForceInput = ParticleVariable;

            //fields.title = "my text";
            //string newfield = JsonUtility.ToJson(fields);
            //Debug.Log(newfield);
        }
        else { }
    }

    [System.Serializable]
    public class _Particle
    {                         //Class defined to obtain the Cloud Variable Name and Result
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
    /*
    public void alert() {

        if (sp.IsOpen)
        {
            try
            {
                sp.Write("1");
                
     
                /*
                if (sp.ReadByte() == 1)
                {

                    transform.Translate(Vector3.left * Time.deltaTime * 5);
                    text_vr.text = "LEFT";
                }
                if (sp.ReadByte() == 2)
                {
                   
                    transform.Translate(Vector3.right * Time.deltaTime * 5);
                    text_vr.text = "RIGHT";
                }
                */
    // }
    //catch (System.Exception)
    // {
    // }
    //  }


    // }
    /*
     public void alert_off()
     {

         if (sp.IsOpen)
         {
             try
             {
                 sp.Write("0");

                 /*
                 if (sp.ReadByte() == 1)
                 {

                     transform.Translate(Vector3.left * Time.deltaTime * 5);
                     text_vr.text = "LEFT";
                 }
                 if (sp.ReadByte() == 2)
                 {

                     transform.Translate(Vector3.right * Time.deltaTime * 5);
                     text_vr.text = "RIGHT";
                 }
                 */
    // }
    // catch (System.Exception)
    //{
    // }
    // }


    // }
    /*
    void Update()
    {
        //Insert your cURL here:
        string url = "https://api.thingspeak.com/channels/444510/feeds.json?results=2";
        www = new WWW(url);
        StartCoroutine(WaitForRequest(www));
        temperature.text = temp;
        humidity.text = hum;
        /*
        if (sp.IsOpen)
        {
            try
            {
                value = sp.ReadLine();
                text_vr.text = value;
                /*
                if (sp.ReadByte() == 1)
                {

                    transform.Translate(Vector3.left * Time.deltaTime * 5);
                    text_vr.text = "LEFT";
                }
                if (sp.ReadByte() == 2)
                {
                   
                    transform.Translate(Vector3.right * Time.deltaTime * 5);
                    text_vr.text = "RIGHT";
                }
                */
        //  }
        // catch (System.Exception)
        //  {
        // }
        // }
    //}
//}