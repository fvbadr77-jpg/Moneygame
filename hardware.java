package com.example.moneygame;

import android.content.Context;
import android.os.Build;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.os.VibratorManager;

public class Hardware {

    // Vibrate the Android device
    public static void vibrate(Context context, long milliseconds) {

        if (context == null) {
            return;
        }

        Vibrator vibrator;

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {

            VibratorManager manager =
                    (VibratorManager) context.getSystemService(
                            Context.VIBRATOR_MANAGER_SERVICE
                    );

            if (manager == null) {
                return;
            }

            vibrator = manager.getDefaultVibrator();

        } else {

            vibrator =
                    (Vibrator) context.getSystemService(
                            Context.VIBRATOR_SERVICE
                    );
        }

        if (vibrator == null || !vibrator.hasVibrator()) {
            return;
        }

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {

            vibrator.vibrate(
                    VibrationEffect.createOneShot(
                            milliseconds,
                            VibrationEffect.DEFAULT_AMPLITUDE
                    )
            );

        } else {

            vibrator.vibrate(milliseconds);
        }
    }


    // Short vibration for button presses
    public static void buttonVibration(Context context) {
        vibrate(context, 40);
    }


    // Longer vibration for events such as rebirth
    public static void rebirthVibration(Context context) {
        vibrate(context, 150);
    }
}
