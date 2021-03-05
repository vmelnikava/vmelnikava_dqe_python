import sys
sys.path.append('D:\\Python_DQE\\Module5')
sys.path.append('D:\\Python_DQE\\Module4')
sys.path.append('D:\\Python_DQE\\Module7')
sys.path.append('D:\\Python_DQE\\Module8')
sys.path.append('D:\\Python_DQE\\Module9')
import publishing_input as pi
import process_batch as pb
import functions as f
import generate_csv
import process_json as pj
import process_xml as px


def select_mode():
    mode = input(f"""Enter which mode you would like to run publishing:
    1 - Input Mode
    2 - Batch Mode
    3 - JSON Mode
    4 - XML Mode
    0 - Exit\nYour Input:\n""")
    return mode


def normalize_file():
    print('\nLog: applying case normalization to newsfeed')
    with open(rf"{pi.default_output_path}\\" + "newsfeed_input.txt", 'r') as file:
        norm_data = f.normalize(file.read())
    norm_data = norm_data.replace('Privatead', 'PrivateAd')
    with open(rf"{pi.default_output_path}\\" + "newsfeed_input.txt", 'w') as file:
        file.write(norm_data)
    print('Log: case normalization was successfully applied!\n')


def main():
    mode = select_mode()
    if mode == '1':
        pi.main()
    elif mode == '2':
        pb.main()
    elif mode == '3':
        pj.main()
    elif mode == '4':
        px.main()
    elif mode == '0':
        pi.good_bye()
    else:
        print('ERROR: incorrect input (1,2,3 or 4 is expected)')
        exit(0)
    normalize_file()
    generate_csv.main(pi.default_output_path, pi.output_file_name)
    pi.good_bye()


main()
