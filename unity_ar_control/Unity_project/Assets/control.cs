using UnityEngine;
using UnityEngine.UI;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;


using System;

public class control : MonoBehaviour
{
    private MqttClient client;
    string temp;
    string hum;
    public string jsonRate;
    WWW www;
    public Text temperature;
    public Text humidity;


    void Start()
    {
        // create client instance 
        client = new MqttClient("demo.thingsboard.io", 1883 , false, null);

        // register to message received 
        client.MqttMsgPublishReceived += client_MqttMsgPublishReceived;

        //connect to client with client id and accesstoken
        client.Connect("ardemo", "wMQkmvzyasQ6MoeUMpLH", null);

    }

    void client_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
    {

        Debug.Log("Received: " + System.Text.Encoding.UTF8.GetString(e.Message));
    }

    /*
     *   
    IEnumerator Req() {
        WWWForm form = new WWWForm();
        form.AddField("field1", "100");

        UnityWebRequest www = UnityWebRequest.Post("https://api.thingspeak.com/update?api_key=TXQVQPD307GC5KYO&", form);
        yield return www.Send();
        Debug.Log("re su");

    }
    IEnumerator Reqq()
    {
        WWWForm form = new WWWForm();
        form.AddField("field1", "50");

        UnityWebRequest www = UnityWebRequest.Post("https://api.thingspeak.com/update?api_key=TXQVQPD307GC5KYO&", form);
        yield return www.Send();
        Debug.Log("re su");

    }
    */
    /*
    //Obtain temperature & humidty value from the thingspeak Cloud using JSON
    IEnumerator WaitForRequest(WWW www)
    {
        yield return www;
        // check for errors
        if (www.error == null)
        {
            string work = www.text;
            //yield return new WaitForSeconds(2);
            // Debug.Log("re su");
            //RootObject fields = JsonUtility.FromJson<RootObject>(work);
            //get temperature value from json
            //jsonRate = fields.feeds[0].field1;
            //temp = jsonRate.Substring(0, 2);
            //get humidity value from json
            //jsonRate = fields.feeds[0].field2;
            //hum = jsonRate.Substring(0, 2);
            //Debug to console
            //Debug.Log(work);
            //yield return new WaitForSeconds(5);
            //Debug.Log(hum);

        }
        else {
            //Debug.Log("not");
        }
    }*/


    //publish on command
    public void on()
    {
        Debug.Log("ON");
       
        Debug.Log("sending...");
        client.Publish("v1/devices/me/attributes", System.Text.Encoding.UTF8.GetBytes("{\"key1\": \"100\"}"));
        Debug.Log("sent");

    }
    //publish off command
    public void off()
    {
        Debug.Log("OFF");

        Debug.Log("sending...");
        client.Publish("v1/devices/me/attributes", System.Text.Encoding.UTF8.GetBytes("{\"key1\": \"50\"}"));
        Debug.Log("sent");

    }

    void Update()
    {
 

    }

}
