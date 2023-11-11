import argparse
import xml.etree.ElementTree as ET
import datetime

def parse_date(date_string):
    try:
        return datetime.datetime.strptime(date_string.split('+')[0].strip(), '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None

def extract_activities(xml_file, year):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    workout_statistics = []
    for element in root.iter('WorkoutStatistics'):
        if element.get('type') == 'HKQuantityTypeIdentifierDistanceWalkingRunning':
            start_date = parse_date(element.get('startDate'))
            if start_date and start_date.year == year:
                workout_record = {
                    'distance': float(element.get('sum')),  # Distance covered in the activity
                    'startDate': element.get('startDate'),
                    'endDate': element.get('endDate')
                }
                workout_statistics.append(workout_record)

    return workout_statistics

def main():
    parser = argparse.ArgumentParser(description='Extract walking or running activities from an XML file.')
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
