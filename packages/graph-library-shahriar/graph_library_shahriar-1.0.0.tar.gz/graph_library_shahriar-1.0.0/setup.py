from setuptools import setup, find_packages

setup(
    name="graph_library_shahriar",                
    version="1.0.0",                  
    author="Shahriar Ahmed",                    
    author_email="shahriarahmed99bd@gmail.com", 
    description="A library for BFS and DFS graph traversal algorithms.",
    long_description=open("README.md").read(), 
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/graph_library", 
    packages=find_packages(),           
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",         
    install_requires=[],                  
    include_package_data=True,         
)