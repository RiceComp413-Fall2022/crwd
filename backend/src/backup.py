from github import Github, InputFileContent

class Backup:
    '''Allows saving/restoring strings using a Github Gist'''

    def __init__(self, access_token: str, gist_id: str, file_name: str):
        '''
        access_token: a github access token with Gist privileges
        gist_id: the id of the gist to save to / read from. 
                 The gist should already be created.
        file_name: the name of the file to use within the gist.
        '''
        self.github = Github(access_token)
        self.gist_id = gist_id
        self.file_name = file_name
        

    def save(self, data: str) -> None:
        '''Saves a string to the target gist.'''
        gist = self.github.get_gist(self.gist_id)
        content = InputFileContent(data)
        gist.edit('Update by backup.py', {self.file_name: content})


    def restore(self) -> str:
        '''Returns the contents of the target gist.'''
        gist = self.github.get_gist(self.gist_id)
        file = gist.files[self.file_name]
        return file.content
