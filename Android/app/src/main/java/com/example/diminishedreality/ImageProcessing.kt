package com.example.diminishedreality

import android.util.Base64
import android.util.Log
import java.io.File
import java.io.FileOutputStream
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.*


object ImageProcessing {

    //Reads a file bytewise, returns Base64 encoded String of this bytes
    fun convertToBase64(attachment: File): String {
        return Base64.encodeToString(attachment.readBytes(), Base64.NO_WRAP)
    }

    //Creates a file from Base64 encoded bytes in the specified directory
    fun base64Decode(base64String: String?, directory: File): File {

        //Decode Base64 String to Byte Array
        val decodedBytes = Base64.decode(base64String, Base64.DEFAULT)

        // Create a File with current date and time as name
        val photo = File(
            directory,
            SimpleDateFormat(
                "yyyy-MM-dd-HH-mm-ss-SSS", Locale.US
            ).format(System.currentTimeMillis()) + ".jpeg")

        if (photo.exists()) {
            photo.delete()
        }

        //Write bytes to photo file using a FileOutputStream
        try {
            val fos = FileOutputStream(photo.path)
            fos.write(decodedBytes)
            fos.close()
        } catch (e: IOException) {
            Log.e("Base64Decode", "Exception in writing file", e)
        }

        return photo
    }
}