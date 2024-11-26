from config import Config
import conversation
import login
import swebdriver

def collect_data_from_tidio(config):
    driver = swebdriver.create_driver(config)
    login.login_to_tidio(config, driver)
    conversation_elements = conversation.collect_conversation_solved_elements_from_tidio(config, driver)
    hrefs = conversation.get_conversation_hrefs(conversation_elements)
    conversation.download_conversations_data_from_tidio(config, hrefs)
    swebdriver.close_driver(driver)

if __name__ == '__main__':
    config = Config()
    conversation.prepare_data_dir()
    is_exist_data_files = conversation.data_dir_has_conversation_data_files()
    if not is_exist_data_files:
        collect_data_from_tidio(config)

    is_merged_data_file = conversation.data_dir_has_merged_conversation_data_file()
    if is_merged_data_file:
        print('Data already merged')
        exit()
    
    conversations_data = conversation.merge_conversations_data_from_tidio()
    conversations_data = conversation.prepare_dict_to_csv(conversations_data)
    conversation.save_merged_conversations_data_to_csv(conversations_data)