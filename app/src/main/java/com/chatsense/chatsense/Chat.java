package com.chatsense.chatsense;

import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioRecord;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.os.Environment;
import android.provider.MediaStore;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;

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

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);

        //Loads the name of the user you're texting
        TextView userTexting = (TextView) findViewById(R.id.userTexting);
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
        filePath = Environment.getExternalStorageDirectory().getPath()+ File.separator +
                "message.pcm";
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
                    initializeEmojiChat();
                }
            }
            catch (Exception e)
            {
                e.printStackTrace();
            }
        }
        if (view.getId() == R.id.playButton)
        {
            stopRecording(view);
            playRecording(view);

        }
    }

    public void onFocusChange(View view, Boolean hasFocus)
    {
        if (!hasFocus)
        stopRecording(view);

    }

    public void initializeEmojiChat()
    {
        View text = LayoutInflater.from(this).inflate(R.layout.emojichat, null);
        LinearLayout chat_history = (LinearLayout) findViewById(R.id.TEXT_HISTORY) ;
        chat_history.addView(text);
    }
}