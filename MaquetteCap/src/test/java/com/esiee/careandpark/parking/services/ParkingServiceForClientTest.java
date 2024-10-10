package com.esiee.careandpark.parking.services;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import com.esiee.careandpark.parking.modele.exceptions.ParkingNotFoundException;

class ParkingServiceForClientTest {

	@Test
	@DisplayName("given parkingName is empty when stationner then return ParkingNotFoundExpetion")
	void stationner_returnParkingNotFound_ifparkingnameisempty() {
		
		String parkingName = "";
		
		 Assertions.assertThrows(ParkingNotFoundException.class, () -> {
			 ParkingServiceForClient parkingServiceForClient = new ParkingServiceForClient();
			 parkingServiceForClient.stationner(parkingName,1);
			  });
	}

}
