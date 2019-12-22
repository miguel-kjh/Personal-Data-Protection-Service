import unittest
import uuid

from app.main import db
from app.main.model.fileLog import FileLog
from app.test.base import BaseTestCase
from app.main.service.LogService import saveLog,getAllLog,getFileToDelete,getByPublicId,updateDelete

class TestLog(BaseTestCase):

    def test_insert(self):
        saveLog({
            'name':'file1',
            'folder':'folder',
            'isdelete':False,
            'filetype':'txt'
        })
        self.assertEqual(len(getAllLog()),1)
        for i in range(2,11):
            saveLog({
                'name':'file'+str(i),
                'folder':'folde2',
                'isdelete':False,
                'filetype':'txt'
            })
        self.assertEqual(len(getAllLog()),10)
    
    def test_getFilterDelete(self):
        saveLog({
            'name':'file1',
            'folder':'folder',
            'isdelete':True,
            'filetype':'txt'
        })
        saveLog({
            'name':'file2',
            'folder':'folder',
            'isdelete':False,
            'filetype':'txt'
        })
        saveLog({
            'name':'file3',
            'folder':'folder',
            'isdelete':True,
            'filetype':'txt'
        })
        self.assertEqual(len(getFileToDelete()),2)
    
    def test_updateDelete(self):
        saveLog({
            'name':'file1',
            'folder':'folder',
            'isdelete':True,
            'filetype':'txt'
        })
        id = saveLog({
            'name':'file2',
            'folder':'folder',
            'isdelete':False,
            'filetype':'txt'
        })
        saveLog({
            'name':'file3',
            'folder':'folder',
            'isdelete':True,
            'filetype':'txt'
        })
        self.assertEqual(getByPublicId(id).isDelete,False)
        updateDelete(id,True)
        self.assertEqual(getByPublicId(id).isDelete,True)
        


if __name__ == '__main__':
    unittest.main()