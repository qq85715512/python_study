# -*- coding: utf-8 -*-
def main():
    file_reader = open('target.csv', 'r', encoding='utf-8')
    file_writer = open('target_output', 'w', encoding='utf-8')
    for line in file_reader:
        line_cells = line.split(',')
        game_id = line_cells[0]
        game_type = line_cells[2]
        game_home = line_cells[3]
        game_guest = line_cells[4]
        game_rst = '1' if line_cells[5] == '胜' else '0'
        key = '_'.join([game_id[:8], game_id[8:], game_type, game_home, game_guest])
        features = '\001'.join(['1', game_rst])
        slot_value_map_str = '\001'.join(['1|' + game_type, '2|' + game_home, '3|' + game_guest])
        values = line_cells[7:]
        slots = [str(x) for x in range(4, len(values) + 4)]
        slot_value_map_str = slot_value_map_str + '\001' + '\001'.join(['|'.join(x) for x in zip(slots, values)])
        features = '\001'.join([features, slot_value_map_str])
        record = '\t'.join([key, features])
        file_writer.writelines(record)

    file_reader.close()
    file_writer.close()





if __name__ == '__main__':
    main()