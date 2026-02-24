import tempfile
import unittest
import sys
import os
import shutil

# Add the directory containing the script to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import standardize_readme

class TestStandardizeReadme(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create .github directory
        os.makedirs('.github')
        
        # Create README_TEMPLATE.md
        with open('.github/README_TEMPLATE.md', 'w', encoding='utf-8') as f:
            f.write("# {REPO_NAME}\n\n{DESCRIPTION}\n")
            
    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)
        
    def test_extract_description_existing_readme(self):
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write("# Title\n\nThis is a test description.\n\nAnother line.\n")
            
        desc = standardize_readme.extract_description('README.md')
        self.assertEqual(desc, "This is a test description.")
        
    def test_extract_description_no_readme(self):
        desc = standardize_readme.extract_description('README.md')
        self.assertEqual(desc, "A new project from MoFA.")
        
    def test_extract_description_skips_headers_and_links(self):
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write("# Title\n<div align=\"center\">\n[Link](url)\n\nActual description.\n")
            
        desc = standardize_readme.extract_description('README.md')
        self.assertEqual(desc, "Actual description.")

    def test_main_execution(self):
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write("# Old Title\n\nOld description.\n")
            
        # Mock get_repo_name since it uses os.path.abspath('.') which is now a temp dir
        original_get_repo_name = standardize_readme.get_repo_name
        standardize_readme.get_repo_name = lambda: "test-repo"
        
        try:
            standardize_readme.main()
            
            with open('README.md', 'r', encoding='utf-8') as f:
                content = f.read()
                
            self.assertIn("# test-repo", content)
            self.assertIn("Old description.", content)
        finally:
            standardize_readme.get_repo_name = original_get_repo_name

if __name__ == '__main__':
    unittest.main()
