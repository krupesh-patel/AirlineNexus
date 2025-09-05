"""
MCP Tools for Flight Operations
Replaces the FastAPI endpoints with direct MCP tool methods
"""

import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Any
from typing import Dict, List, Optional

from mcp.server.fastmcp import FastMCP

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("flight-mcp-server")

# Create server instance
mcp = FastMCP("airlinenexus-flight-server")

from config.database import db_manager

logger = logging.getLogger(__name__)


class FlightMCPTools:
    """MCP Tools for flight operations without HTTP API dependency"""

    def __init__(self):
        self.db_manager = db_manager

    def search_flights_impl(self,
                            departure_airport: Optional[str] = None,
                            arrival_airport: Optional[str] = None,
                            departure_date: Optional[str] = None,
                            passengers: int = 1,
                            class_preference: str = "economy") -> Dict[str, Any]:
        """Search for available flights based on criteria"""
        try:
            # Generate mock flight data based on search criteria
            flights = self._generate_flight_results(
                departure_airport, arrival_airport, departure_date, passengers, class_preference
            )

            return {
                'success': True,
                'flights': flights,
                'total_results': len(flights),
                'search_criteria': {
                    'departure_airport': departure_airport,
                    'arrival_airport': arrival_airport,
                    'departure_date': departure_date,
                    'passengers': passengers,
                    'class_preference': class_preference
                }
            }

        except Exception as e:
            logger.error(f"Flight search error: {e}")
            return {
                'success': False,
                'error': str(e),
                'flights': []
            }

    def get_flight_details_impl(self, flight_number: str) -> Dict[str, Any]:
        """Get detailed information about a specific flight"""
        try:
            # Generate flight details based on flight number
            flight_details = self._generate_flight_details(flight_number)

            if flight_details:
                return {
                    'success': True,
                    'flight': flight_details
                }
            else:
                return {
                    'success': False,
                    'error': f'Flight {flight_number} not found'
                }

        except Exception as e:
            logger.error(f"Flight details error: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def create_booking_impl(self,
                            flight_number: str,
                            passenger_name: str,
                            passenger_email: str,
                            phone_number: Optional[str] = None,
                            special_requests: Optional[str] = None) -> Dict[str, Any]:
        """Create a flight booking"""
        try:
            # Generate booking reference
            booking_reference = self._generate_booking_reference()

            # Get flight details
            flight_result = self.get_flight_details_impl(flight_number)
            if not flight_result['success']:
                return flight_result

            flight = flight_result['flight']

            # Create booking record
            booking = {
                'booking_reference': booking_reference,
                'flight_number': flight_number,
                'passenger_name': passenger_name,
                'passenger_email': passenger_email,
                'phone_number': phone_number,
                'special_requests': special_requests,
                'booking_date': datetime.now().isoformat(),
                'status': 'confirmed',
                'flight_details': flight,
                'total_price': flight.get('price', 299)
            }

            # Store booking (in production, would save to database)
            self._store_booking(booking)

            return {
                'success': True,
                'booking': booking,
                'message': f'Booking confirmed! Reference: {booking_reference}'
            }

        except Exception as e:
            logger.error(f"Booking creation error: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def get_booking_status_impl(self, booking_reference: str) -> Dict[str, Any]:
        """Get booking status and details"""
        try:
            # Retrieve booking (in production, would query database)
            booking = self._retrieve_booking(booking_reference)

            if booking:
                return {
                    'success': True,
                    'booking': booking
                }
            else:
                return {
                    'success': False,
                    'error': f'Booking {booking_reference} not found'
                }

        except Exception as e:
            logger.error(f"Booking status error: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def cancel_booking_impl(self, booking_reference: str) -> Dict[str, Any]:
        """Cancel a booking"""
        try:
            # Retrieve booking first
            booking = self._retrieve_booking(booking_reference)

            if not booking:
                return {
                    'success': False,
                    'error': f'Booking {booking_reference} not found'
                }

            # Update booking status
            booking['status'] = 'cancelled'
            booking['cancellation_date'] = datetime.now().isoformat()

            # Store updated booking
            self._store_booking(booking)

            return {
                'success': True,
                'booking': booking,
                'message': f'Booking {booking_reference} has been cancelled'
            }

        except Exception as e:
            logger.error(f"Booking cancellation error: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def _generate_flight_results(self, departure: str, arrival: str, date: str, passengers: int, class_pref: str) -> \
            List[Dict[str, Any]]:
        """Generate mock flight search results"""
        flights = []

        # Generate 2 flight options
        for i in range(3, 5):
            airline = "AirlineNexus"
            flight_number = "AN" + str(100 + i)

            # Calculate departure and arrival times
            base_time = datetime.now() + timedelta(days=1)
            departure_time = base_time.replace(hour=6 + i * 2, minute=0, second=0)
            arrival_time = departure_time + timedelta(hours=3 + i * 0.5)

            # Price varies by class
            base_price = 200 + i * 50
            if class_pref == 'business':
                base_price *= 2.5
            elif class_pref == 'first':
                base_price *= 4

            flight = {
                'flight_number': flight_number,
                'airline': "AirlineNexus",
                'departure_airport': departure or 'JFK',
                'arrival_airport': arrival or 'LAX',
                'departure_time': departure_time.isoformat(),
                'arrival_time': arrival_time.isoformat(),
                'duration': '5h 30m',
                'aircraft': 'Boeing 737-800',
                'price': int(base_price * passengers),
                'currency': 'USD',
                'available_seats': 45 - i * 5,
                'class': class_pref,
                'stops': 0 if i < 3 else 1,
                'status': 'available'
            }

            flights.append(flight)

        return flights

    def _generate_flight_details(self, flight_number: str) -> Optional[Dict[str, Any]]:
        """Generate detailed flight information"""
        # Extract airline code from flight number
        airline_code = flight_number[:2]

        airline_name = "AirlineNexus"

        # Generate departure/arrival times
        departure_time = datetime.now() + timedelta(days=1, hours=8)
        arrival_time = departure_time + timedelta(hours=5, minutes=30)

        return {
            'flight_number': flight_number,
            'airline': airline_name,
            'departure_airport': 'JFK',
            'departure_city': 'New York',
            'arrival_airport': 'LAX',
            'arrival_city': 'Los Angeles',
            'departure_time': departure_time.isoformat(),
            'arrival_time': arrival_time.isoformat(),
            'duration': '5h 30m',
            'aircraft': 'Boeing 737-800',
            'terminal_departure': '4',
            'terminal_arrival': '2',
            'gate_departure': 'A12',
            'gate_arrival': 'B8',
            'status': 'on_time',
            'price': 299,
            'currency': 'USD',
            'available_seats': 42,
            'class_options': ['economy', 'business', 'first'],
            'amenities': ['WiFi', 'In-flight Entertainment', 'Meals', 'Power Outlets']
        }

    def _generate_booking_reference(self) -> str:
        """Generate a unique booking reference"""
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def _store_booking(self, booking: Dict[str, Any]) -> None:
        """Store booking (mock implementation)"""
        # In production, this would save to database
        # For demo, we'll just log it
        logger.info(f"Stored booking: {booking['booking_reference']}")

    def _retrieve_booking(self, booking_reference: str) -> Optional[Dict[str, Any]]:
        """Retrieve booking (mock implementation)"""
        # Mock booking data for demo
        if booking_reference in ['ABC123', 'XYZ789']:
            return {
                'booking_reference': booking_reference,
                'flight_number': 'AN101',
                'passenger_name': 'John Doe',
                'passenger_email': 'john.doe@email.com',
                'booking_date': datetime.now().isoformat(),
                'status': 'confirmed',
                'total_price': 299,
                'flight_details': self._generate_flight_details('AN101')
            }
        return None


# Initialize the flight tools instance
flight_tools = FlightMCPTools()


# MCP Tool Functions
@mcp.tool()
def search_flights(departure_airport: Optional[str] = None,
                   arrival_airport: Optional[str] = None,
                   departure_date: Optional[str] = None,
                   passengers: int = 1,
                   class_preference: str = "economy") -> Dict[str, Any]:
    """
    Search for available flights based on criteria
    
    Args:
        departure_airport: Airport code (e.g., 'JFK', 'LAX')
        arrival_airport: Airport code (e.g., 'JFK', 'LAX') 
        departure_date: Date in YYYY-MM-DD format
        passengers: Number of passengers
        class_preference: 'economy', 'business', or 'first'
        
    Returns:
        Dict with flight search results
    """
    return flight_tools.search_flights_impl(
        departure_airport, arrival_airport, departure_date, passengers, class_preference
    )


@mcp.tool()
def get_flight_details(flight_number: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific flight
    
    Args:
        flight_number: Flight number (e.g., 'AN101')
        
    Returns:
        Dict with flight details
    """
    return flight_tools.get_flight_details_impl(flight_number)


@mcp.tool()
def create_booking(flight_number: str,
                   passenger_name: str,
                   passenger_email: str,
                   phone_number: Optional[str] = None,
                   special_requests: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a flight booking
    
    Args:
        flight_number: Flight number to book
        passenger_name: Primary passenger name
        passenger_email: Passenger email
        phone_number: Contact phone number
        special_requests: Any special requests
        
    Returns:
        Dict with booking confirmation
    """
    return flight_tools.create_booking_impl(
        flight_number, passenger_name, passenger_email, phone_number, special_requests
    )


@mcp.tool()
def get_booking_status(booking_reference: str) -> Dict[str, Any]:
    """
    Get booking status and details
    
    Args:
        booking_reference: Booking reference code
        
    Returns:
        Dict with booking status
    """
    return flight_tools.get_booking_status_impl(booking_reference)


@mcp.tool()
def cancel_booking(booking_reference: str) -> Dict[str, Any]:
    """
    Cancel a booking
    
    Args:
        booking_reference: Booking reference to cancel
        
    Returns:
        Dict with cancellation status
    """
    return flight_tools.cancel_booking_impl(booking_reference)


# Global instance
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
