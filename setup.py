import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="streamlit_supabase_auth",
    version="1.0.2",
    author="Han Qiao",
    author_email="sweatybridge@gmail.com",
    description="JWT authentication with Supabase",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sweatybridge/streamlit-supabase-auth",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 1.32.0",
        "google-search-results >=2.4.2",
        "requests==2.31.0",
        "requests-oauthlib==1.3.1",
        "tiktoken==0.6.0",
        "openai==1.13.3",
        "loguru==0.7.2",
        "supabase==2.4.0",
        "PyJWT==2.8.0",
        "anthropic==0.19.1",
    ],
)
