package com.esiee.careandpark.parking.modele;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import com.esiee.careandpark.parking.modele.reference.TypePlace;

class ParkingTest {
	
	
	@Test
	void testCreationParkingMalInitie() {
		
		 Assertions.assertThrows(InstantiationError.class, () -> {
			  new Parking(-1, 0, 0, 0,"");
		});
	}
	
	@Test
	void testCreationParkingadresseNull() {
		
		 Assertions.assertThrows(InstantiationError.class, () -> {
			  new Parking(0, 0, 0, 0,null);
		});
	}
	
	@Test
	void testCreationParkingSansPlace_returnParkingWithListePlaceVide() {
		Parking parking = new Parking(0, 0, 0, 0,"");
		
		List<Place> places = parking.getPlaces();
		assertTrue(places.isEmpty(), "il ne doit pas y avoir de place");

	}
	
	@Test
	void testCreationParkingWithOnlyNormalPlace() {
		Parking parking = new Parking(2, 0, 0, 0,"");
		
		List<Place> places = parking.getPlaces();
		assertEquals(2,places.size(), "il  doit y avoir 2 place");
		
		for(Place place : places) {
			assertEquals(TypePlace.NOMINALE,place.getType(), "La place doit être normale");
		}

	}
	

	@Test
	void testCreationParkingWithOnlyHandicapePlace() {
		Parking parking = new Parking(0, 2, 0, 0,"");
		
		List<Place> places = parking.getPlaces();
		assertEquals(2,places.size(), "il  doit y avoir 2 place");
		
		for(Place place : places) {
			assertEquals(TypePlace.HANDICAPE,place.getType(), "La place doit être handicape");
		}

	}
	
	@Test
	void testCreationParkingWithOnlyBusPlace() {
		Parking parking = new Parking(0, 0, 2, 0,"");
		
		List<Place> places = parking.getPlaces();
		assertEquals(2,places.size(), "il  doit y avoir 2 place");
		
		for(Place place : places) {
			assertEquals(TypePlace.BUS,place.getType(), "La place doit être BUS");
		}

	}
	
	@Test
	void testCreationParkingWithOnly2roues() {
		Parking parking = new Parking(0, 0, 0, 2,"");
		
		List<Place> places = parking.getPlaces();
		assertEquals(2,places.size(), "il  doit y avoir 2 place");
		
		for(Place place : places) {
			assertEquals(TypePlace.DEUX_ROUES,place.getType(), "La place doit être 2 ROUES");
		}

	}

	@Test
	void testSearchPlaceLibreWithNoPlace_returnEmptyList() {
		Parking parking = new Parking(0, 0, 0, 0,"");
		
		List<Place> places = parking.searchPlaceLibre(TypePlace.NOMINALE);
		assertTrue(places.isEmpty(), "il ne doit pas y avoir de place de libres");
	}

}
