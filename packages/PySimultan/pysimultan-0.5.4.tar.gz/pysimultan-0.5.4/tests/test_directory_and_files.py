import os
from PySimultan2.src.PySimultan2 import DataModel
from PySimultan2.src.PySimultan2.files import FileInfo, DirectoryInfo


project_dir = os.environ.get('PROJECT_DIR', '/simultan_projects')
if not os.path.exists(project_dir):
    os.makedirs(project_dir)

new_data_model = DataModel.create_new_project(project_path=os.path.join(project_dir, 'test_dir_files.simultan'),
                                              user_name='admin',
                                              password='admin')

print(new_data_model.file_directories)


new_directory_info = DirectoryInfo(path='directory_info_dir',
                                   data_model=new_data_model)

print(new_data_model.file_directories)

print(new_directory_info.resource_entry)
print(new_directory_info.parent)

new_file1 = new_directory_info.add_file('test_add_file.txt', 'This is a test file')
new_file2 = new_directory_info.add_file('test_add_file2.txt')

sub_directory_info = new_directory_info.add_sub_directory('sub_dir')
print(sub_directory_info.parent)

print(new_directory_info.sub_directories)


new_directory = new_data_model.create_resource_directory('test_dir')
new_directory2 = new_data_model.create_resource_directory('test_dir2')
new_directory4 = new_data_model.create_resource_directory('test_dir3')

new_data_model.add_empty_resource(filename=os.path.join(new_directory.CurrentFullPath, 'test_empty_file.txt'))

new_data_model.add_empty_resource(filename='test_empty_file2.txt',
                                  target_dir=new_directory)

new_file_info0 = FileInfo.from_string(filename='test_file.txt',
                                      content='This is a test file',
                                      data_model=new_data_model)

new_file_info = FileInfo.from_string(filename='test_file.txt',
                                     content='This is a test file',
                                     target_dir=new_directory,
                                     data_model=new_data_model)

new_file_info2 = FileInfo.from_string(filename='test_file2.txt',
                                     content='This is a test file 2',
                                     target_dir=new_directory2.current_full_path,
                                     data_model=new_data_model)

# create just a file in the directory
with open(os.path.join(new_directory2.current_full_path, 'not_contained_test_file3.txt'), 'w') as f:
    f.write('This is a test file 3')


new_data_model.save()
new_data_model.cleanup()
