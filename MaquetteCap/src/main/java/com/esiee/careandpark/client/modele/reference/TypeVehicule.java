package com.esiee.careandpark.client.modele.reference;

import com.esiee.careandpark.parking.modele.reference.TypePlace;

public enum TypeVehicule {
	Voiture, Van, Bus, Moto, Velo, Scooter;

	public TypePlace getTypePlace() {
		switch (this) {
		case Moto:
			return TypePlace.DEUX_ROUES;
		case Velo:
			return TypePlace.DEUX_ROUES;
		case Scooter:
			return TypePlace.DEUX_ROUES;
		case Van:
			return TypePlace.BUS;
		case Bus:
			return TypePlace.BUS;
		default:
			return TypePlace.NOMINALE;
		}
	}
}
