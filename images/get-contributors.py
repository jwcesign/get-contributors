#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import requests
import argparse
import logging
import os
import shutil

from git.repo import Repo
from bs4 import BeautifulSoup


def parseParameter():
    parser = argparse.ArgumentParser(description='Get repo contributors')
    parser.add_argument('--repo', type=str, required=True, help='Repo address, like: https://github.com/karmada-io/karmada.git')
    parser.add_argument('--start', type=str, required=True, help='The start tag/commit flag')
    parser.add_argument('--end', type=str, required=True, help='The end tag/commit flag')
    parser.add_argument('--exclude_contributor', nargs='+', type=str, required=False, help='The contributor to ignore, use space to split')
    args = parser.parse_args()
    return args.repo, args.start, args.end, args.exclude_contributor


def get_contribution_info(repo, commits, exclude):
    base_url = repo.remote().url
    base_url = base_url.removesuffix(".git") + "/commit/"
    nick_name = {}
    contributors = {}
    not_ok_commit = []
    for id in commits:
        if commits[id] in nick_name.keys():
            continue
        if exclude is not None and commits[id] in exclude:
            logging.info("Ignore contributor:%s", commits[id])
            continue
        resp = requests.get(base_url+id)
        page = BeautifulSoup(resp.content, 'html.parser')
        tracks = page.find_all('img', attrs={'class': 'avatar-user', 'data-test-selector': 'commits-avatar-stack-avatar-image'})
        if len(tracks) == 0:
            not_ok_commit.append(id)
            continue
        ctr = BeautifulSoup(str(tracks[0]), 'html.parser').find('img').get('alt')
        logging.info("Find contributor match:%s/%s", commits[id], ctr)
        contributors[ctr] = ""
        nick_name[commits[id]] = ""

    sorted_data = sorted(contributors.keys(), key=lambda x:x.lower())
    logging.info("-"*30)
    data = "\n"
    for i in sorted_data:
        data += i + "\n"
    logging.info("Total contributor:%d %s", len(sorted_data), data)   
    logging.info("-"*30)

    if len(not_ok_commit) != 0:
        logging.info("Following commit not ok, please visit and check")
        for i in not_ok_commit:
            logging.info(base_url+i)

def list_all_commits(repo, start, end):
    logging.info("Start to get all commits")
    commitIds = {}
    for commit in repo.iter_commits(rev=start+"..."+end):
        commitIds[commit.hexsha] = commit.author.name

    return commitIds

def clone_repo(repo: str):
    logging.info("Start to clone repo:%s", repo)
    if os.path.exists("./repo"):
        shutil.rmtree("./repo")
    newest_code = Repo.clone_from(repo, "./repo")
    return newest_code

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    repo, start, end, exclude_contributors = parseParameter()
    repo_clone = clone_repo(repo)
    commits = list_all_commits(repo_clone, start, end)
    get_contribution_info(repo_clone, commits, exclude_contributors)
    