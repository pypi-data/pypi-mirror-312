# -*- coding: utf-8 -*-
# @Time    : 2024/7/11 12:03
# @Author  : Quanfa
# @Desc    : new version

#region import
from .path_tool import MyPath
from .project import Project
import sys
#endregion

def pickle_save(object, path: MyPath):
    import pickle
    MyPath(path).ensure()
    with open(path, 'wb') as f:
        pickle.dump(object, f)
        
def pickle_load(path: MyPath):
    import pickle
    with open(path, 'rb') as f:
        return pickle.load(f)
    
def auto_suffix(name: str, suffix: str = None) -> str:
    if suffix == '':
        return name
    return name + '.' + suffix

class ScriptFileSaver:
    #region static properties
    project_path = None

    #endregion

    def __init__(self, script_file, locals, version: int = 1):
        """
        An advisor for script assets.

        Args:
            script_file (str): __file__, the path of the script.
            locals (dict): local params, usually locals().
            version (int, optional): version, if None, point to new version. Defaults to '1'.
        """
        #region core properties
        self.locals = locals
        self.script_path = MyPath.from_file(script_file)
        self.version = version
        #endregion

        #region prelauch task, trigger once
        if ScriptFileSaver.project_path is None:  # type: ignore
            project_path = Project.from_folder(self.script_path.get_parent())
            sys.path.append(project_path)  # append project path to system 
            sys.path.append(self.script_path.get_parent())
            ScriptFileSaver.project_path = project_path
            
            try:
                import torch
                def my_repr(tensor, d=1):
                    return f'Tensor{tuple(tensor.shape)}-{tensor.device.__str__()}|{str(tensor.dtype)[6:]}:{((tensor*100).round()/100).cpu().detach().numpy()}'
                torch.Tensor.__repr__ = my_repr
            except:
                pass
        #endregion
        self.package_path = self.script_path.get_parent()
        if locals['__package__'] in ['', None]:
            locals['__package__'] = self.package_path.relative_to(ScriptFileSaver.project_path)[1:].replace('/', '.')
        
    #region properties functioned

    @property
    def save_path_parent(self):
        return self.script_path.get_parent().cat(f'_l_{self.script_name}_v{self.version}')  # save path

    @property
    def script_name(self):
        return self.script_path.get_name()[:-3]  # remove .py

    #endregion

    def __getitem__(self, name):
        return self.path_of(name)

    def path_of(self, name: str, suffix: str = None) -> MyPath:
        """
        advice the path of the object.

        Args:
            name (str): name of the object.
            suffix (str): if None, use the type of the object.

        Returns:
            path(MyPath): the path of the object.
        """
        if suffix is None:
            suffix = str(type(self.locals[name])).split("'")[1].split('.')[-1]

        return self.save_path_parent.cat(auto_suffix(name, suffix))

    def end_script(self, show=True):
        """
        mark the end of the script.
        """
        if not self.save_path_parent.exist():
            return
        stored_file = self.save_path_parent.cat('__init__.py')
        
        with open(stored_file, 'w') as f:
            f.write(
"""
from EsyPro import MyPath
src_path = MyPath(__file__).get_parent()        
"""
            )
            
            for file in self.save_path_parent.get_files(''):
                name = file.replace('.', '_')

                if name.startswith('__'):
                    continue
                f.write(f"{name} = src_path.cat('{file}')\n")
        
        if show:
            print(f'All the code in {self.script_name} has been done')

    def save(self, object, name: str=None, suffix: str = 'pkl', path=None):
        if path is None:
            path = self.path_of(name, suffix).ensure()
        pickle_save(object, path)
    
    def load(self, name: str=None, suffix: str = None, path=None):
        if path is None:
            path = self.path_of(name, suffix)
        path = MyPath(path)
        if not path.exist():
            return None
        return pickle_load(path)
    
    def auto_date(self, result_path: MyPath, annotate=''):
        """
        Generates a unique folder name based on the current date and checks for existing folders with the same name to avoid overwriting. if annotate is True, a __init__.py file will be created in the folder to store the script name and experiment time. Then, add record to csv file under the result_path.
        Args:
            result_path (MyPath): The base path where the new folder will be created.
        Returns:
            result_folder (Mypath): A new path object pointing to the unique folder created.
        """
        import datetime
        exp_name = 'exp' + datetime.datetime.now().strftime('%Y%m%d')  
        repeat_exp = 0
        result_folder = result_path.cat(exp_name + f'_{repeat_exp}')
        while result_folder.exist():
            repeat_exp += 1
            result_folder = result_path.cat(exp_name + f'_{repeat_exp}')
        
        exp_name = exp_name + f'_{repeat_exp}'
        result_folder = result_path.cat(exp_name)
            
        if annotate is not None:
            result_folder.ensure()
            annotate_file = result_folder.cat('__init__.py')
            with open(annotate_file, 'w') as f:
                f.write(f"""
import EsyPro
src_path = EsyPro.MyPath(__file__).get_parent()
script_name = '{self.script_path}'
exp_time = '{exp_name}'
annotate = '{annotate}'
                        """)
            record_csv = result_path.cat('exp_record.csv')
            if not record_csv.exist():
                with open(record_csv, 'w') as f:
                    f.write('exp_name,script_name,annotate\n')
            with open(record_csv, 'a') as f:
                f.write(f'{exp_name},{self.script_path},{annotate}\n')
        return result_folder