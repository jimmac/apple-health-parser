import argparse
import xml.sax
import datetime

class WorkoutStatisticsHandler(xml.sax.ContentHandler):
    def __init__(self, target_year):
        self.target_year = target_year
        self.activities = []

    def startElement(self, name, attrs):
        if name == 'WorkoutStatistics':
            if attrs['type'] == 'HKQuantityTypeIdentifierDistanceWalkingRunning':
                start_date = self.parse_date(attrs['startDate'])
                if start_date and start_date.year == self.target_year:
                    self.activities.append({
                        'distance': float(attrs['sum']),
                        'startDate': attrs['startDate'],
                        'endDate': attrs['endDate']
                    })

    def parse_date(self, date_string):
        try:
            return datetime.datetime.strptime(date_string.split('+')[0].strip(), '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None

def extract_activities(xml_file, year):
    handler = WorkoutStatisticsHandler(year)
    xml.sax.parse(xml_file, handler)
    return handler.activities

def main():
    parser = argparse.ArgumentParser(description='Extract walking or running activities from an XML file using SAX parser.')
    parser.add_argument('year', type=int, help='The year for which to extract activities')
    parser.add_argument('xml_file', type=str, help='Path to the XML file')
    args = parser.parse_args()

    activities = extract_activities(args.xml_file, args.year)
    total_distance = sum(activity['distance'] for activity in activities)

    print(f"Year: {args.year}")
    print(f"Number of Activities: {len(activities)}")
    print(f"Total Distance: {total_distance:.2f} km")

if __name__ == "__main__":
    main()
