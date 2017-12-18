import org.apache.commons.http.client.fluent;

public class Test {
	public static void main(String args[]){
		Request.Get("http://targethost/homepage").execute().returnContent();
		Request.Post("http://targethost/login")
				.bodyForm(Form.form().add("username",  "vip").add("password",  "secret").build())
				.execute().returnContent();
	}
}
