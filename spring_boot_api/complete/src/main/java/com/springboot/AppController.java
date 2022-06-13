package com.example.springboot;

import org.json.simple.JSONObject;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import com.opencsv.CSVReader;
import com.opencsv.exceptions.CsvValidationException;

import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;
import java.io.*;
import java.io.FileReader;
import java.io.File;
import java.io.FileNotFoundException;

@RestController
public class AppController {

	@GetMapping("/")
	public String index() {
		return "Endpoints: /average_mass, /year_with_most_falls";
	}

	@GetMapping("/year_with_most_falls")
	public @ResponseBody JSONObject get_year_with_most_falls() {

		List<List<String>> records = new ArrayList<List<String>>();
		try {
			String filePath = new File("results.csv").getAbsolutePath();
			CSVReader csvReader = new CSVReader(new FileReader(filePath));
			String[] values = null;
			while ((values = csvReader.readNext()) != null) {
				records.add(Arrays.asList(values));
			}
			csvReader.close();

			JSONObject return_val = new JSONObject();
			return_val.put(records.get(2).get(1).replace(" ", "_"), records.get(2).get(0));
			return return_val;

		} catch (IOException e) {
			System.out.println("An error occurred.");
			e.printStackTrace();
		} catch (CsvValidationException e) {
			System.out.println("An error occurred.");
			e.printStackTrace();
		}

		JSONObject return_val = new JSONObject();
		return return_val;

	}

	@GetMapping("/average_mass")
	public @ResponseBody JSONObject get_average_mass() {

		List<List<String>> records = new ArrayList<List<String>>();
		try {
			String filePath = new File("results.csv").getAbsolutePath();
			CSVReader csvReader = new CSVReader(new FileReader(filePath));
			String[] values = null;
			while ((values = csvReader.readNext()) != null) {
				records.add(Arrays.asList(values));
			}
			csvReader.close();

			JSONObject return_val = new JSONObject();
			return_val.put(records.get(1).get(1).replace(" ", "_"), records.get(1).get(0));
			return return_val;

		} catch (IOException e) {
			System.out.println("An error occurred.");
			e.printStackTrace();
		} catch (CsvValidationException e) {
			System.out.println("An error occurred.");
			e.printStackTrace();
		}

		JSONObject return_val = new JSONObject();
		return return_val;

	}

}



