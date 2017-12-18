import org.apache.commons.httpclient.HttpClient;
import org.apache.commons.httpclient.HttpException;
import org.apache.commons.httpclient.HttpStatus;
import org.apache.commons.httpclient.methods.PostMethod;
import org.apache.http.impl.client.HttpClients;

public class PostReqEx {

  public void sendReq(String url, String name, int howmany){
    HttpClient httpClient = HttpClients.createDefault();
    PostMethod postMethod = new PostMethod(url);
    postMethod.addParameter("name", name);
    postMethod.addParameter("num_msg", howmany);
    try {
        httpClient.executeMethod(postMethod);
    } catch (HttpException e) {
        e.printStackTrace();
    } catch (IOException e) {
        e.printStackTrace();
    }

    if (postMethod.getStatusCode() == HttpStatus.SC_OK) {
        String resp = postMethod.getResponseBodyAsString();
    } else {
         //...postMethod.getStatusLine();
    }
  }

	public static void main(String args[]){
		String url = "https://chatsense.pythonanywhere.com/getback";
		String name = "ECR";
		int howmany = 20;
		sendReq(url, name, howmany);
	}

}
