FROM gitpod/workspace-full

RUN sudo apt-get update  
&& sudo apt-get install -y     tool  
&& sudo rm -rf /var/lib/apt/lists/*

RUN sudo apt-get update && \
    sudo apt-get install -y r-base

RUN sudo R -e "install.packages('arsenal', repos='http://cran.rstudio.com/')"
&& sudo R -e "install.packages('questionr', repos='http://cran.rstudio.com/')"