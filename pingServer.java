package pingServer;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;


public class pingServer
{
	 private static String lineEnd = "\r\n";
	 private static String twoHyphens = "--";
	 private static String boundary = "AaB03x87yxdkjnxvi7";
	 private static URL url;
	   
	public static void main(String args[]) throws IOException
	{
		upload();
	}

	public static void upload() throws IOException 
	{
		HttpURLConnection conn = null;
		DataOutputStream dos = null;
		DataInputStream dis = null;
		FileInputStream fileInputStream = null;
		String fileParameterName = "C:\\Users\\Charlie\\Desktop\\speech\\strange.wav";
		url = new URL("http://chatsense.pythonanywhere.com/send");
		byte[] buffer;
		int maxBufferSize = 20 * 1024;
		try {
			//client request
			File file = new File(fileParameterName);
			fileInputStream = new FileInputStream(file);

			// open a URL connection to the Servlet
			// Open a HTTP connection to the URL
			conn = (HttpURLConnection) url.openConnection();
			// Allow inputs
			conn.setDoInput(true);
			// Allow outputs
			conn.setDoOutput(true);
			// Don't use a cached copy
			conn.setUseCaches(false);
			// Use a post method
			conn.setRequestMethod("POST");
			conn.setRequestProperty("Content-Type", "Sending file");

			dos = new DataOutputStream(conn.getOutputStream());

			// create a buffer of maximum size
			buffer = new byte[Math.min((int) file.length(), maxBufferSize)];
			int length;
			// read file and write it into form
			while ((length = fileInputStream.read(buffer)) != -1) {
				dos.write(buffer, 0, length);
			}

			//send form data necessary after file data
			dos.writeBytes(lineEnd);
			dos.writeBytes(twoHyphens + boundary + twoHyphens + lineEnd);
			dos.flush();
			} finally {
				if (fileInputStream != null) fileInputStream.close();
				if (dos != null) dos.close();
			}

		//reads the server response
		try {
			dis = new DataInputStream(conn.getInputStream());
			StringBuilder response = new StringBuilder();

			String line;
			while ((line = dis.readLine()) != null) {
				response.append(line).append('\n');
			}

			System.out.println(response.toString());
		} finally {
			if (dis != null) dis.close();
		}

	}
}