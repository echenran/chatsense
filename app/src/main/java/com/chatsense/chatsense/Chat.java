package com.chatsense.chatsense;

import android.graphics.Color;
import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioRecord;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.os.AsyncTask;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.rockerhieu.emojicon.EmojiconTextView;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;



public class Chat extends AppCompatActivity implements  View.OnClickListener{

    boolean doRun = true;
    boolean isRecording = false;

    /**Constant**/
    public static final int SAMPLER_RATE = 44100;
    public static final int BUFFER_ELEM_TO_REC = 1024;
    public static final int BYTES_PER_ELEM = 2; //It's 16 bit, so 2 bytes

    AudioRecord recorder = null;
    Thread recordingThread = null;
    public String filePath;

    String returnData;

    //Loads the name of the user you're texting
    TextView userTexting;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);

        userTexting = (TextView) findViewById(R.id.userTexting);
        Bundle extras = getIntent().getExtras();
        userTexting.setText(extras.getString("whose_mans"));

        //Progress bar
        final ProgressBar progress = (ProgressBar) findViewById(R.id.progressBar);
        progress.setProgress(0);

        //Recording button
        final Button recordButton = (Button) findViewById(R.id.record);
        recordButton.setOnClickListener(this);

        final ImageButton playButton = (ImageButton) findViewById(R.id.playButton);
        playButton.setOnClickListener(this);

    }


    public void startRecording(View view) throws IOException
    {
        /**Records audio, outputs .mp3 file**/
        recorder = new AudioRecord(MediaRecorder.AudioSource.MIC, SAMPLER_RATE, AudioFormat.CHANNEL_IN_MONO,
                AudioFormat.ENCODING_PCM_16BIT, BUFFER_ELEM_TO_REC*BYTES_PER_ELEM);

        recorder.startRecording();
        isRecording = true;

        recordingThread = new Thread(new Runnable() {
            public void run()
            {
                writeAudioDataToFile();
            }
        }, "AudioRec thread");

        recordingThread.start();

    }

    //convert short to byte
    private byte[] short_to_byte(short[] sData) {
        int shortArrsize = sData.length;
        byte[] bytes = new byte[shortArrsize * 2];
        for (int i = 0; i < shortArrsize; i++) {
            bytes[i * 2] = (byte) (sData[i] & 0x00FF);
            bytes[(i * 2) + 1] = (byte) (sData[i] >> 8);
            sData[i] = 0;
        }
        return bytes;

    }

    private void writeAudioDataToFile() {
        filePath = Environment.getExternalStorageDirectory().getPath()+ File.separator + "message.pcm";
        short sData[] = new short[BUFFER_ELEM_TO_REC];
        /** Java can't use shorts, need to convert to bytes**/

        FileOutputStream os = null;
        try {
            os = new FileOutputStream(filePath);
        } catch (FileNotFoundException e)
        {
            e.printStackTrace();
        }

        while (isRecording) {
            recorder.read(sData, 0,BUFFER_ELEM_TO_REC);
            try {
                byte bData[] = short_to_byte(sData);
                os.write(bData,0,BUFFER_ELEM_TO_REC*BYTES_PER_ELEM);
            }
            catch (IOException e)
            {
                e.printStackTrace();
            }
        }
        try {
            os.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void playRecording(View view)
    {
        try {
            MediaPlayer player = new MediaPlayer();
            player.setDataSource(filePath);
            player.setAudioStreamType(AudioManager.STREAM_MUSIC);
            player.prepare();
            player.start();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }

    public void stopRecording(View view)
    {
        if (null != recorder) {
            isRecording = false;
            recorder.stop();
            recorder.release();
            recorder = null;
            recordingThread = null;
        }
    }

    boolean notRunning = true;

    public void onClick(View view)
    {
        if (view.getId() == R.id.record) {
            try {
                if (!isRecording) {
                    startRecording(view);
                }
            }
            catch (Exception e)
            {
                e.printStackTrace();
            }
        }
        if (view.getId() == R.id.playButton)
        {
            if (isRecording) {
                stopRecording(view);

                SendFeedbackJob job = new SendFeedbackJob();
                job.execute();

                try {
                    while (returnData == null)
                    {
                        Thread.sleep(1000);
                    }
                    initializeEmojiChat(returnData);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }

            }
        }
    }

    public void onFocusChange(View view, Boolean hasFocus)
    {
        if (!hasFocus)
        stopRecording(view);

    }
    private class SendFeedbackJob extends AsyncTask<Void, Void, String> {

        @Override
        protected String doInBackground(Void... voids) {
            String s = "";
            try {
                s = PingServer.upload();
            }
            catch (Exception e) {
            e.printStackTrace();
            }

            returnData = s;
            return s;
        }
    }


    public void initializeEmojiChat(String data) throws InterruptedException {
        returnData = null;
        View text = LayoutInflater.from(this).inflate(R.layout.emojichat, null);
        LinearLayout chat_history = (LinearLayout) findViewById(R.id.TEXT_HISTORY) ;
        chat_history.addView(text);

        String textVar = data.split(":")[1].split(",")[0];

        textVar = textVar.substring(2,textVar.length()-1);

        String time = data.split(": ")[2].split(",")[0];
        time = time.substring(1,time.length()-1);

        Integer anger = Integer.parseInt(data.split(": ")[5].split(",")[0]);
        Integer neutrality = Integer.parseInt(data.split(": ")[6].split(",")[0]);
        Integer sadness = Integer.parseInt(data.split(": ")[7].split(",")[0]);
        Integer fear = Integer.parseInt(data.split(": ")[8].split(",")[0]);
        Integer happiness = Integer.parseInt(data.split(": ")[9].substring(0,1));

        EmojiconTextView emoji = (EmojiconTextView) text.findViewById(R.id.emoji);
        Button bubble = (Button) text.findViewById(R.id.chat_bubble);
        TextView date = (TextView) text.findViewById(R.id.date);

        bubble.setText(textVar);
        date.setText(time);
        emoji.setText(getEmojiFromValues(neutrality,happiness,sadness,anger,fear));
    //    bubble.setBackgroundColor(getColorFromValues(neutrality,happiness,sadness,anger,fear));*/

    }

    public String getEmojiFromValues(int neutral, int happy, int sad, int angry, int fear) {
        String NEUTRAL = "\uD83D\uDE36";

        String[] SAD = {"\uD83D\uDE14","\uD83D\uDE1E","\uD83D\uDE2D"};

        String[] FEAR = {"\uD83D\uDE2C","\uD83D\uDE28","\uD83D\uDE31"};

        String[] HAPPY = {"\uD83D\uDE0A","\uD83D\uDE03","\uD83D\uDE02"};

        String[] ANGRY = {"\uD83D\uDE12","\uD83D\uDE20","\uD83D\uDE21"};

        int i;
        if (neutral > 85)
        {
            return NEUTRAL;
        }
        if (neutral > 55)
        {
            i = 0;
        }
        if (neutral > 35)
        {
            i = 1;
        }
        else
        {
            i = 2;
        }


        int max = Integer.max(Integer.max(sad, happy),Integer.max(angry, fear));
        if (happy == max)
        {
            return HAPPY[i];
        }
        if (sad == max)
        {
            return SAD[i];
        }
        if (angry == max)
        {
            return ANGRY[i];
        }
        if (fear == max)
        {
            return FEAR[i];
        }


        return NEUTRAL;
    }
}