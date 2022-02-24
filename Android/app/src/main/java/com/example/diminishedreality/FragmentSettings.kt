package com.example.diminishedreality

import android.graphics.Color
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.Spinner
import androidx.navigation.fragment.findNavController
import com.example.diminishedreality.databinding.FragmentFirstBinding
import android.widget.AdapterView

import androidx.core.view.isVisible


/**
 * A simple [Fragment] subclass as the default destination in the navigation.
 */
class FragmentSettings : Fragment() {

    //create binding for interaction with UI controls
    private var _binding: FragmentFirstBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {

        _binding = FragmentFirstBinding.inflate(inflater, container, false)
        return binding.root

    }

    //use bundle for storing selected configuration
    val bundle = Bundle()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        binding.buttonFirst.setOnClickListener {
            //navigate to FragmentCamera
            findNavController().navigate(R.id.action_FirstFragment_to_SecondFragment, bundle)
        }

        binding.btnObjects.setOnClickListener {
            //show object selector
            binding.textviewFirst.isVisible = true
            binding.btnColors.isChecked = false
            binding.toggleGroupColor.isVisible = false
            binding.spinnerObjects.isVisible = true
            binding.textviewFirst.text = "Select an object to diminish"
            binding.buttonFirst.isEnabled = true

            bundle.putString("selectedMode", "object")
        }

        binding.btnColors.setOnClickListener {
            //show color selector
            binding.textviewFirst.isVisible = true
            binding.btnObjects.isChecked = false
            binding.toggleGroupColor.isVisible = true
            binding.spinnerObjects.isVisible = false
            binding.textviewFirst.text = "Select a color to diminish"

            bundle.putString("selectedMode", "color")
        }

        binding.btnRed.setOnClickListener {
            //configure red color selection
            binding.buttonFirst.isEnabled = true
            binding.btnRed.isChecked = true
            binding.btnGreen.isChecked = false
            binding.btnBlue.isChecked = false
            binding.btnRed.background.setTint(Color.parseColor("#ff8585"))
            binding.btnGreen.background.setTint(Color.parseColor("#d4f0ce"))
            binding.btnBlue.background.setTint(Color.parseColor("#b8cff5"))

            bundle.putString("selectedColor", "red")
        }

        binding.btnGreen.setOnClickListener {
            //configure green color selection
            binding.buttonFirst.isEnabled = true
            binding.btnRed.isChecked = false
            binding.btnGreen.isChecked = true
            binding.btnBlue.isChecked = false
            binding.btnRed.background.setTint(Color.parseColor("#ffc2c2"))
            binding.btnGreen.background.setTint(Color.parseColor("#92d982"))
            binding.btnBlue.background.setTint(Color.parseColor("#b8cff5"))

            bundle.putString("selectedColor", "green")
        }

        binding.btnBlue.setOnClickListener {
            //configure blue color selection
            binding.buttonFirst.isEnabled = true
            binding.btnRed.isChecked = false
            binding.btnGreen.isChecked = false
            binding.btnBlue.isChecked = true
            binding.btnRed.background.setTint(Color.parseColor("#ffc2c2"))
            binding.btnGreen.background.setTint(Color.parseColor("#d4f0ce"))
            binding.btnBlue.background.setTint(Color.parseColor("#79a8f2"))

            bundle.putString("selectedColor", "blue")
        }

        //spinner for selection of objects to remove from the image
        val spinner: Spinner = binding.spinnerObjects
        spinner.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(
                adapterView: AdapterView<*>, view: View?,
                position: Int, id: Long
            ) {
                val item = adapterView.getItemAtPosition(position)
                if (item != null) {
                    bundle.putString("selectedObject", item.toString())
                }
            }

            override fun onNothingSelected(adapterView: AdapterView<*>?) {}
        }
        //Create ArrayAdapter to fill spinner with objects from resource array
        ArrayAdapter.createFromResource(
            this.requireContext(),
            R.array.objects_array,
            android.R.layout.simple_spinner_item
        ).also { adapter ->
            adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
            spinner.adapter = adapter
        }
    }



    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}