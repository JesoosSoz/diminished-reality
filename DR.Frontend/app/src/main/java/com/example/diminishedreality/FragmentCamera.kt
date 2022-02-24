package com.example.diminishedreality

import android.Manifest
import android.app.Activity
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.provider.MediaStore
import android.util.Log
import android.util.Size
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.camera.core.CameraSelector
import androidx.camera.core.ImageCapture
import androidx.camera.core.ImageCaptureException
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.core.content.ContextCompat
import androidx.core.view.isVisible
import androidx.navigation.fragment.findNavController
import com.example.diminishedreality.databinding.FragmentSecondBinding
import kotlinx.android.synthetic.main.fragment_second.*
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.text.SimpleDateFormat
import java.util.*
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors
import kotlin.collections.HashMap
import android.provider.DocumentsContract

import android.content.ContentUris

import android.os.Environment

import android.os.Build
import java.io.FileOutputStream
import java.io.InputStream
import java.io.OutputStream


/**
 * A simple [Fragment] subclass as the second destination in the navigation.
 *
 * https://developer.android.com/codelabs/camerax-getting-started#1
 */
class FragmentCamera : Fragment() {

    //set liveView to true for continuous image capture and processing
    private val liveView: Boolean = false

    private var _binding: FragmentSecondBinding? = null
    private var imageCapture: ImageCapture? = null
    private lateinit var outputDirectory: File
    private lateinit var cameraExecutor: ExecutorService
    private lateinit var safeContext: Context

    //create binding for interaction with UI controls
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {

        //start camera when view is created
        startCamera()

        outputDirectory = getOutputDirectory()

        cameraExecutor = Executors.newSingleThreadExecutor()

        _binding = FragmentSecondBinding.inflate(inflater, container, false)
        return binding.root

    }

    override fun onAttach(context: Context) {
        super.onAttach(context)
        safeContext = context
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        binding.buttonSecond.setOnClickListener {
            //navigate back to FragmentSettings
            findNavController().navigate(R.id.action_SecondFragment_to_FirstFragment)
        }
        binding.cameraCaptureButton.setOnClickListener {
            //set viewFinder for live camera stream visible
            binding.viewFinder.isVisible = true
            binding.imageViewGallery.isVisible = false
            takePhoto()
        }
        binding.buttonGallery.setOnClickListener {
            //set imageView for displaying local image file visible
            binding.viewFinder.isVisible = false
            binding.imageViewGallery.isVisible = true
            getImageFromGallery()
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
        cameraExecutor.shutdown()
    }


    //open gallery for image selection
    //show all image formats to select from
    private val REQUEST_CODE = 100
    private fun getImageFromGallery() {
        val intent = Intent(Intent.ACTION_PICK)
        intent.type = "image/*"
        startActivityForResult(intent, REQUEST_CODE)
    }

    //when image is selected from gallery, show original image and send it to backend
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (resultCode == Activity.RESULT_OK && requestCode == REQUEST_CODE){
            //shutdown camera if local image file is selected
            stopCamera()

            imageViewGallery.setImageURI(data?.data) // handle chosen image

            val imageUri = data?.data

            //read selected image and write it as file to working directory
            val inp: InputStream? = imageUri?.let { safeContext.contentResolver.openInputStream(it) }
            val outFile = File(
                outputDirectory,
                SimpleDateFormat(FILENAME_FORMAT, Locale.US
                ).format(System.currentTimeMillis()) + ".jpg")
            val out: OutputStream = FileOutputStream(outFile)
            val buf = ByteArray(1024)
            var len: Int
            if (inp != null) {
                while (inp.read(buf).also { len = it } > 0) {
                    out.write(buf, 0, len)
                }
            }
            out.close()
            inp?.close()

            //get selected mode from arguments and call function accordingly
            if (outFile != null) {
                if (arguments?.getString("selectedMode").toString() == "object") {
                    getDiminishedImageInpaint(outFile)
                }
                else if (arguments?.getString("selectedMode").toString() == "color") {
                    getDiminishedImageColor(outFile)
                }
            }
        }
    }


    //Get one image from camera
    //see: https://medium.com/swlh/how-to-create-a-simple-camera-app-using-android-camerax-library-7367778498e0
    private fun takePhoto() {
        // Get a stable reference of the modifiable image capture use case
        val imageCapture = imageCapture ?: return

        // Create time-stamped output file to hold the image
        val photoFile = File(
            outputDirectory,
            SimpleDateFormat(FILENAME_FORMAT, Locale.US
            ).format(System.currentTimeMillis()) + ".jpg")

        // Create output options object which contains file + metadata
        val outputOptions = ImageCapture.OutputFileOptions.Builder(photoFile).build()

        // Set up image capture listener, which is triggered after photo has
        // been taken
        imageCapture.takePicture(
            outputOptions, ContextCompat.getMainExecutor(safeContext), object : ImageCapture.OnImageSavedCallback {
                override fun onError(exc: ImageCaptureException) {
                    Log.e(TAG, "Photo capture failed: ${exc.message}", exc)
                }

                override fun onImageSaved(output: ImageCapture.OutputFileResults) {
                    val savedUri = Uri.fromFile(photoFile)
                    val msg = "Photo capture succeeded: $savedUri"
                    //Toast.makeText(safeContext, msg, Toast.LENGTH_SHORT).show()
                    Log.d(TAG, msg)

                    if (arguments?.getString("selectedMode").toString() == "object") {
                        getDiminishedImageInpaint(photoFile)
                    }
                    else if (arguments?.getString("selectedMode").toString() == "color") {
                        getDiminishedImageColor(photoFile)
                    }


                }
            }
        )
    }

    private fun startCamera() {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(safeContext)

        cameraProviderFuture.addListener(Runnable {
            // Used to bind the lifecycle of cameras to the lifecycle owner
            val cameraProvider: ProcessCameraProvider = cameraProviderFuture.get()

            // Preview
            val preview = Preview.Builder()
                .build()
                .also {
                    it.setSurfaceProvider(viewFinder.surfaceProvider)
                }

            // Select back camera as a default
            val cameraSelector = CameraSelector.DEFAULT_BACK_CAMERA

            try {
                // Unbind use cases before rebinding
                cameraProvider.unbindAll()

                // Bind use cases to camera
                cameraProvider.bindToLifecycle(
                    this, cameraSelector, preview, imageCapture)

            } catch(exc: Exception) {
                Log.e(TAG, "Use case binding failed", exc)
            }

        }, ContextCompat.getMainExecutor(safeContext))

        imageCapture = ImageCapture.Builder().setTargetResolution(Size(270, 160))
            .build()
    }

    private fun stopCamera() {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(safeContext)
        // Used to bind the lifecycle of cameras to the lifecycle owner
        val cameraProvider: ProcessCameraProvider = cameraProviderFuture.get()
        // Unbind use cases
        cameraProvider.unbindAll()
    }


    //send image file to backend and apply inpainting
    fun getDiminishedImageInpaint(file: File) {
        //Base64 encode file
        val base64String = ImageProcessing.convertToBase64(file)
        //get selected object from settings
        val diminishingObject = arguments?.getString("selectedObject")

        //create json representation for body of request
        val jsonMap = HashMap<String, String>()
        jsonMap["image"] = base64String
        if (diminishingObject != null) {
            jsonMap["object"] = "[\"$diminishingObject\"]" //pass object as list
        }

        //send HTTP request in separate thread
        Thread {
            val diminishedString = DiminishingAPI.post("http://10.0.2.2:5000/inpaint", JSONObject(
                jsonMap as Map<*, *>
            ).toString(), false)

            val diminishedJSON = JSONObject(diminishedString)

            //create and show file from returned json string
            val diminishedFile = ImageProcessing.base64Decode(diminishedJSON["image"].toString(), getOutputDirectory())
            showImage(Uri.fromFile(diminishedFile))
        }.start()
    }

    fun getDiminishedImageColor(file: File) {
        //Base64 encode file
        val base64String = ImageProcessing.convertToBase64(file)
        //get selected color from settings
        val diminishingColor = arguments?.getString("selectedColor")

        //create json representation for body of request
        val jsonMap = HashMap<String, String>()
        jsonMap["image"] = base64String
        if (diminishingColor != null) {
            jsonMap["color"] = diminishingColor.toString()
        }

        //send HTTP request in separate thread
        Thread {
            val diminishedString = DiminishingAPI.post("http://10.0.2.2:5000/filtercolor", JSONObject(
                jsonMap as Map<*, *>
            ).toString(), false)

            val diminishedJSON = JSONObject(diminishedString)

            //create and show file from returned json string
            val diminishedFile = ImageProcessing.base64Decode(diminishedJSON["image"].toString(), getOutputDirectory())
            showImage(Uri.fromFile(diminishedFile))
        }.start()
    }

    //get file from uri and show it
    private fun showImage(uri: Uri) {
        activity?.runOnUiThread {
            binding.imageView.setImageURI(uri)
        }

        if (liveView) {
            Thread.sleep(120)
            takePhoto()
        }
    }


    //get working directory for storing and reading images
    private fun getOutputDirectory(): File {
        val mediaDir = safeContext.externalMediaDirs.firstOrNull()?.let {
            File(it, resources.getString(R.string.app_name)).apply { mkdirs() } }
        return if (mediaDir != null && mediaDir.exists())
            mediaDir else safeContext.filesDir
    }

    override fun onDestroy() {
        super.onDestroy()
        cameraExecutor.shutdown()
    }

    companion object {
        private const val TAG = "CameraXBasic"
        private const val FILENAME_FORMAT = "yyyy-MM-dd-HH-mm-ss-SSS"
    }

}