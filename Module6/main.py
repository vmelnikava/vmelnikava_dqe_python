import sys
sys.path.append('D:\\Python_DQE\\Module5')
sys.path.append('D:\\Python_DQE\\Module4')
sys.path.append('D:\\Python_DQE\\Module7')
sys.path.append('D:\\Python_DQE\\Module8')
import publishing_input as pi
import process_batch as pb
import functions as f
import generate_csv
import process_json as pj


def select_mode():
    mode = input(
        f"""Enter which mode you would like to run publishing:\n1 - Input Mode\n2 - Batch Mode\n3 - JSON Mode\n\nYour Input:\n""")
    return mode


def normalize_file():
    print('Log: applying case normalization to newsfeed')
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
    else:
        print('ERROR: incorrect input (1,2 or 3 is expected)')
        exit(0)
    normalize_file()
    generate_csv.main(pi.default_output_path, pi.output_file_name)
    pi.good_bye()


main()
