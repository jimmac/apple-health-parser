import argparse
import xml.sax
import datetime

# Add a minimum speed threshold for running (adjust as needed)
MIN_RUNNING_PACE_SECONDS_PER_KM = 360  # 6 minutes per kilometer

class WorkoutStatisticsHandler(xml.sax.ContentHandler):
    def __init__(self, target_year):
        self.target_year = target_year
        self.activities = []
        self.total_distance = 0.0
        self.total_duration = datetime.timedelta()
        self.total_heart_rate = 0
        self.total_heart_rate_samples = 0

    def startElement(self, name, attrs):
        if name == 'WorkoutStatistics':
            if attrs['type'] == 'HKQuantityTypeIdentifierDistanceWalkingRunning':
                start_date = self.parse_date(attrs['startDate'])
                if start_date and start_date.year == self.target_year:
                    distance = float(attrs['sum'])
                    end_date = self.parse_date(attrs['endDate'])
                    duration = end_date - start_date
                    pace_seconds_per_km = duration.total_seconds() / distance if distance > 0 else None
                    heart_rate = self.parse_heart_rate(attrs.get('averageHeartRate', None))

                    # Adjust the condition to classify as running
                    if pace_seconds_per_km is not None and pace_seconds_per_km < MIN_RUNNING_PACE_SECONDS_PER_KM:
                        return  # Skip, considered as walking

                    self.activities.append({
                        'distance': distance,
                        'startDate': attrs['startDate'],
                        'endDate': attrs['endDate'],
                        'duration': duration,
                        'heartRate': heart_rate
                    })

                    self.total_distance += distance
                    self.total_duration += duration
                    if heart_rate is not None:
                        self.total_heart_rate += heart_rate
                        self.total_heart_rate_samples += 1

    def parse_date(self, date_string):
        try:
            return datetime.datetime.strptime(date_string.split('+')[0].strip(), '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None

    def parse_heart_rate(self, heart_rate_string):
        try:
            return int(heart_rate_string)
        except (ValueError, TypeError):
            return None

def extract_activities(xml_file, year):
    handler = WorkoutStatisticsHandler(year)
    xml.sax.parse(xml_file, handler)
    return handler.activities

import argparse
import xml.sax
import datetime

# Add a minimum speed threshold for running (adjust as needed)
MIN_RUNNING_PACE_SECONDS_PER_KM = 360  # 6 minutes per kilometer

class WorkoutStatisticsHandler(xml.sax.ContentHandler):
    def __init__(self, target_year):
        self.target_year = target_year
        self.activities = []
        self.total_distance = 0.0
        self.total_duration = datetime.timedelta()
        self.total_heart_rate = 0
        self.total_heart_rate_samples = 0

    def startElement(self, name, attrs):
        if name == 'WorkoutStatistics':
            if attrs['type'] == 'HKQuantityTypeIdentifierDistanceWalkingRunning':
                start_date = self.parse_date(attrs['startDate'])
                if start_date and start_date.year == self.target_year:
                    distance = float(attrs['sum'])
                    end_date = self.parse_date(attrs['endDate'])
                    duration = end_date - start_date
                    pace_seconds_per_km = duration.total_seconds() / distance if distance > 0 else None
                    heart_rate = self.parse_heart_rate(attrs.get('averageHeartRate', None))

                    # Adjust the condition to classify as running
                    if pace_seconds_per_km is not None and pace_seconds_per_km < MIN_RUNNING_PACE_SECONDS_PER_KM:
                        return  # Skip, considered as walking

                    self.activities.append({
                        'distance': distance,
                        'startDate': attrs['startDate'],
                        'endDate': attrs['endDate'],
                        'duration': duration,
                        'heartRate': heart_rate
                    })

                    self.total_distance += distance
                    self.total_duration += duration
                    if heart_rate is not None:
                        self.total_heart_rate += heart_rate
                        self.total_heart_rate_samples += 1

    def parse_date(self, date_string):
        try:
            return datetime.datetime.strptime(date_string.split('+')[0].strip(), '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None

    def parse_heart_rate(self, heart_rate_string):
        try:
            return int(heart_rate_string)
        except (ValueError, TypeError):
            return None

def extract_activities(xml_file, year):
    handler = WorkoutStatisticsHandler(year)
    xml.sax.parse(xml_file, handler)
    return handler.activities

def main():
    parser = argparse.ArgumentParser(description='Extract running activities from an XML file using SAX parser.')
    parser.add_argument('year', type=int, help='The year for which to extract running activities')
    parser.add_argument('xml_file', type=str, help='Path to the XML file')
    args = parser.parse_args()

    activities = extract_activities(args.xml_file, args.year)
    total_distance = sum(activity['distance'] for activity in activities)
    total_duration = sum(activity['duration'].total_seconds() for activity in activities)
    total_heart_rate = sum(activity['heartRate'] for activity in activities if activity['heartRate'] is not None)
    total_heart_rate_samples = sum(1 for activity in activities if activity['heartRate'] is not None)

    average_pace_seconds_per_km = total_duration / total_distance if total_distance > 0 else None
    average_heart_rate = total_heart_rate / total_heart_rate_samples if total_heart_rate_samples > 0 else None

    if average_pace_seconds_per_km is not None:
        average_pace_minutes, average_pace_seconds = divmod(int(average_pace_seconds_per_km), 60)
        average_pace_formatted = f"{average_pace_minutes:02d}:{average_pace_seconds:02d}"
    else:
        average_pace_formatted = "N/A"

    print(f"Year: {args.year}")
    print(f"Number of Running Activities: {len(activities)}")
    print(f"Total Running Distance: {total_distance:.2f} km")
    print(f"Average Running Pace: {average_pace_formatted} per kilometer")
    print(f"Average Heart Rate: {average_heart_rate} beats per minute" if average_heart_rate is not None else "No heart rate data available")

if __name__ == "__main__":
    main()

