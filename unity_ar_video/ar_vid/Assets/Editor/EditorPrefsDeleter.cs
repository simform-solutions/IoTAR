using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;

public class EditorPrefsDeleter : Editor
{

	[MenuItem("Help/Reset EULA", false, 111)]
	public static void DeleteEULA()
	{
		EditorPrefs.DeleteKey("EULA_AGREEMENT_ACCEPTED_VERSIONS");
	}
}
