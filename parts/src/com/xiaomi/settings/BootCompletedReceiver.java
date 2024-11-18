/*
 * Copyright (C) 2024 The LineageOS Project
 *
 * SPDX-License-Identifier: Apache-2.0
 */

package com.xiaomi.settings;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.provider.Settings;
import android.util.Log;

public class BootCompletedReceiver extends BroadcastReceiver {
    private static final String TAG = "XiaomiParts";
    private static final boolean DEBUG = true;
    private static final String KEY_MIN_REFRESH_RATE = "min_refresh_rate";

    @Override
    public void onReceive(final Context context, Intent intent) {
        if (!Intent.ACTION_BOOT_COMPLETED.equals(intent.getAction())) {
            return;
        }
        if (DEBUG) {
            Log.d(TAG, "Received boot completed intent");
        }

        // Set the minimum refresh rate to 60Hz
        try {
            Settings.System.putFloat(context.getContentResolver(), KEY_MIN_REFRESH_RATE, 60);
            if (DEBUG) {
                Log.d(TAG, "Successfully set " + KEY_MIN_REFRESH_RATE + " to 60Hz");
            }
        } catch (Exception e) {
            Log.e(TAG, "Failed to set " + KEY_MIN_REFRESH_RATE + " to 60Hz", e);
        }
    }
}
