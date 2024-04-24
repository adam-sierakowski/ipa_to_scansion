import re
import csv


def preprocess_ipa(input_ipa_string):
    clitic_preposition = "(?<=(ˈ|ˌ| ))(v|f|z|s)ʲ?(?=‿)"  # "w" domu, "z" bogiem. Wsześniejszy regex: "(?<=(ˈ|ˌ|\b))(v|f|z|s)ʲ?(?=‿)" pominął ",w niebiosy", "w :arszawie", "w krakowie":
    html_1 = "<sup>"
    html_2 = "</sup>"  # there could be more HTML tags
    preprocessed_ipa = re.sub(clitic_preposition, "∅", input_ipa_string)
    preprocessed_ipa = preprocessed_ipa.replace(html_1, "")
    preprocessed_ipa = preprocessed_ipa.replace(html_2, "")
    return preprocessed_ipa


def scan_verse(input_ipa_string):
    cursor = '˩'
    scanned_string = ""
    last_phoneme = ""

    for char in input_ipa_string:

        if char == 'ː':  # geminate
            if last_phoneme in vowels:
                if cursor == '˩':
                    scanned_string += 's'
                elif cursor == '˥':
                    scanned_string += 'S'
                    cursor = '˩'

        if char in vowels:
            if cursor == '˩':
                scanned_string += 's'
            elif cursor == '˥':
                scanned_string += 'S'
                cursor = '˩'
        elif char == 'ˌ' or char == 'ˈ':
            cursor = '˥'
        elif char == ' ':
            scanned_string += ' '
        elif char == '‿':
            scanned_string += '‿'
        elif char == '∅':
            scanned_string += '∅'

        if char in phonemes:
            last_phoneme = char

    return scanned_string


def clear_scansion(input_scansion_string):
    chars_to_clear = [" ", "∅", "‿"]
    cleared_scansion = input_scansion_string
    for char in chars_to_clear:
        cleared_scansion = cleared_scansion.replace(char, "")
    return cleared_scansion


consonants = {'b', 'c', 'd', 'f', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'x', 'z', 'ŋ', 'ɕ', 'ɟ',
              'ɡ',
              'ɲ', 'ʃ', 'ʑ', 'ʒ', 'ʣ', 'ʤ', 'ʥ', 'ʦ', 'ʧ', 'ʨ', 'ʲ', 'γ', 'ḍ', 'ṭ',
              'b', 'c', 'd', 'f', 'g', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'x', 'z', 'ŋ', 'ɕ', 'ɟ', 'ɡ', 'ɣ', 'ɲ', 'ɾ', 'ʂ', 'ʃ', 'ʑ', 'ʒ', 'ʔ', 'ʣ', 'ʤ', 'ʥ', 'ʦ', 'ʧ', 'ʨ', 'γ', 'ḍ', 'ṭ'}
vowels = {'a', 'e', 'i', 'u', 'ã', 'ä', 'ü', 'ĩ', 'ũ', 'ɔ', 'ɛ', 'ɨ', 'a', 'e', 'i', 'o', 'u', 'â', 'ã', 'ä', 'æ', 'ø', 'ü', 'ĩ', 'ũ', 'ɑ', 'ɔ', 'ə', 'ɛ', 'ɨ', 'ɪ', 'ɯ'}
phonemes = consonants.union(vowels)

input_csv = "sorted_output_file.csv"
output_csv = "output_scansion.csv"

with open(input_csv, "r") as input_csv_file:
    reader = csv.reader(input_csv_file)

    with open(output_csv, "w") as output_csv_file:
        writer = csv.writer(output_csv_file)

        header = ["id", "orthographic", "IPA", "detailed_scansion", "simple_scansion"]
        writer.writerow(header)

        for row in reader:
            ipa = row[2]
            pprocd_ipa = preprocess_ipa(ipa)
            detailed_scansion = scan_verse(pprocd_ipa)
            simple_scansion = clear_scansion(detailed_scansion)
            row.append(detailed_scansion)
            row.append(simple_scansion)
            writer.writerow(row)

        output_csv_file.flush()


# all_ipas_string = """ˈʧ̑wɔvʲjɛk ˈsṭʃɛla ˈpãn‿buk ˈːulɛ ˈnɔɕi
# ˈʧ̑ɛkaj ˈtatka ˈlatka ˈːʃ kɔˈbɨwkɛ ˈvʲilʦ̑ɨ ˈzʲjɛʣ̑ɔ̃w̃
# pʃɛs‿ˈpãnɨ dɔ‿ˈkrula ˌː‿pʃɛsʲ‿ˈɕfʲjɛ̃ntɛ dɔ‿ˈbɔɡa
# ˈʥ̑ɛ̇ʨ̑i ː‿ˈrɨbɨ ˈɡwɔsu ɲɛ‿ˈmajɔ̃w̃
# ˈdaw ˈpãn‿buɡ ˈzɛ̃mbɨ ˈda i‿ˈxlɛp
# ˈktɔ ˈɲɛ‿ma ˈv‿ɡwɔvʲjɛ ˈtɛ̃n ˈma ˈv‿nɔɡax
# ˈktɔ ˈɕɛ̇jɛ ˈvʲjatr̥ ˈtɛ̃n ˈzbʲjɛra ˈbuʒɛ
# ˈxlɛp ˈpʲivɔ i‿ˈɕfʲjeʦ̑a ˈzdɔbʲjɔ̃w̃ ʃlaxʲˈʨ̑iʦ̑a
# ˈxʦ̑ɔ̃nʦ̑ ˈpɔznaʨ̑ ˌpʃɨjäˈʨ̑ɛla ˈṭʃɛba ˈzʲ‿ɲĩm ˈbɛʧ̑kɛ ˈsɔlʲi ˈzʲjɛ̇ɕʨ
# a‿ˈʦ̑ɔ pɔ‿ˈʧ̑ɨjɛ̇j vʲjɛlˈkɔɕʨ̑i ˈjäc ˈɲɛ‿ma ˈv‿ɡwɔvʲjɛ mɔ̃nˈdrɔɕʨ̑i
# ˌna‿zwɔˈʥ̑ɛ̇ju ˈʧ̑apka ˈɡɔrɛ
# ˈxlɛp i‿ˈvɔda ˈɲɛ‿ma ˈɡwɔda
# aˈpɛtɨt ˈrɔɕɲɛ ˈv‿mʲjarɛ jɛˈʣ̑ɛ̃ɲa
# ˈnɔʦ̑ ãnˈḍʒɛja ɕfʲjɛ̃nˈtɛɡɔ pʃɨ̃ˈɲɛ̇ɕɛ‿nãm ˌnaʒɛʧ̑ɔ̃ˈnɛɡɔ
# ˈwaska ˈpãj̃ska na‿ˈpstrɨ̃m ˈkɔ̃ɲu ˈjɛ̇ʑʥ̑i
# ˈlɛkːɔ ˈpʃɨʃwɔ ˈlɛkːɔ ˈpɔʃwɔ
# ˈvʲjɛ̃nʦ̑ɛj ˌpɔ<sup>w</sup>ufaˈwɔɕʨ̑i ˈɲiʒ ˌznajɔ̃ˈmɔɕʨ̑i
# pãŋˈkraʦ̑ɨ sɛrˈvaʦ̑ɨ ˌbɔ̃ɲiˈfaʦ̑ɨ ˈkaʒdɨ ˈsfɔ<sup>j</sup>ĩmʲ ˈʑĩmnɛ̃m ˈraʧ̑ɨ"""
#
# all_ipas = all_ipas_string.split("\n")
#
# for ipa in all_ipas:
#     pproced = preprocess_ipa(ipa)
#     scansion = scan_verse(pproced)
#     print(scansion)
#
# print("\n\n\n")
#
# for ipa in all_ipas:
#     pproced = preprocess_ipa(ipa)
#     scansion = scan_verse(pproced)
#     cleared_scansion = clear_scansion(scansion)
#     print(cleared_scansion)

