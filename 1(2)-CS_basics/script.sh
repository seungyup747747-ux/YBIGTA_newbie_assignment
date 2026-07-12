
# anaconda(또는 miniconda)가 존재하지 않을 경우 설치해주세요!
if ! command -v conda &> /dev/null; then
    if [[ -x "$HOME/miniconda3/bin/conda" ]]; then
        echo "[INFO] Miniconda가 이미 설치되어 있습니다."
        source "$HOME/miniconda3/etc/profile.d/conda.sh"
    else
        echo "[INFO] conda가 없어 Miniconda를 설치합니다."

        if [[ "$(uname)" == "Darwin" ]]; then
            if [[ "$(uname -m)" == "arm64" ]]; then
                MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh"
            else
                MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
            fi
        else
            MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
        fi

        curl -L "$MINICONDA_URL" -o miniconda.sh
        bash miniconda.sh -b -p "$HOME/miniconda3"
        rm miniconda.sh

        source "$HOME/miniconda3/etc/profile.d/conda.sh"
    fi
else
    CONDA_BASE=$(conda info --base)
    source "$CONDA_BASE/etc/profile.d/conda.sh"
fi


# Conda 환셩 생성 및 활성화
if conda env list | awk '{print $1}' | grep -qx "myenv"; then
    echo "[INFO] myenv 환경이 이미 존재합니다."
else
    conda create -y -n myenv python=3.11
fi

conda activate myenv

## 건드리지 마세요! ##
python_env=$(python -c "import sys; print(sys.prefix)")
if [[ "$python_env" == *"/envs/myenv"* ]]; then
    echo "[INFO] 가상환경 활성화: 성공"
else
    echo "[INFO] 가상환경 활성화: 실패"
    exit 1 
fi

# 필요한 패키지 설치
python -m pip install --upgrade pip
python -m pip install mypy

mkdir -p output

# Submission 폴더 파일 실행
cd submission || { echo "[INFO] submission 디렉토리로 이동 실패"; exit 1; }

for file in *.py; do
    problem_number="${file##*_}"
    problem_number="${problem_number%.py}"
    python "$file" < "../input/${problem_number}_input" > "../output/${problem_number}_output"
done

# mypy 테스트 실행 및 mypy_log.txt 저장
python -m mypy . > ../mypy_log.txt 2>&1

# conda.yml 파일 생성
conda env export --no-builds > ../conda.yml

# 가상환경 비활성화
conda deactivate