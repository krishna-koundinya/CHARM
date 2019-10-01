# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 01:28:03 2019

@author: koundinya

"""
import re

skipset = set()


def lexicOrder(str1, str2):
    r_str = ""
    new_str = sorted([str1, str2])
    r_str += new_str[0] + ',' + new_str[1]
    return r_str


def replaceInItems(curr, target, mapp):
    templ = []
    for k in mapp.keys():
        if curr in k:
            templ.append(k)
    for ki in templ:
        val = mapp.get(ki)
        mapp.pop(ki)
        new_ki = re.sub(curr, target, ki)
        new_ki = new_ki + ''
        mapp[new_ki] = val


def charmProperty(xi, xj, prop_y, minSup, nodes, newN):
    if len(prop_y) >= minSup:
        if (set(nodes.get(xi)) == set(nodes.get(xj))):
            skipset.add(xj)
            tempo = lexicOrder(xi, xj)
            replaceInItems(xi, tempo, newN)
            replaceInItems(xi, tempo, nodes)
            return tempo
        elif (set(nodes.get(xi, {})).issubset(set(nodes.get(xj, {})))):
            tempo = lexicOrder(xi, xj)
            replaceInItems(xi, tempo, newN)
            replaceInItems(xi, tempo, nodes)
            return tempo
        elif (set(nodes.get(xj, {})).issubset(set(nodes.get(xi, {})))):
            skipset.add(xj)
            newN[lexicOrder(xi, xj)] = prop_y
        else:
            if (set(nodes.get(xi, {})) != set(nodes.get(xj, {}))):
                newN[lexicOrder(xi, xj)] = prop_y
    return xi


def isSubsumed(c, y):
    for val in c.values():
        if val == y:
            return True
    return False


def charmExtended(nodes, c, minSup):
    items = list(nodes.keys())
    for idx1 in range(len(items)):
        xi = items[idx1]
        if xi in skipset:
            continue
        x_prev = xi
        x = ''
        newN = {}
        for idx2 in range(idx1 + 1, len(items)):
            xj = items[idx2]
            if xj in skipset:
                continue
            x = lexicOrder(xi, xj)
            y = nodes.get(xi, {})
            temp = set()
            temp = temp.union(y)
            temp = temp.intersection(nodes.get(xj, {}))
            xi = charmProperty(xi, xj, temp, minSup, nodes, newN)
        if newN:
            charmExtended(newN, c, minSup)
        if (x_prev and nodes.get(x_prev) and not isSubsumed(c, nodes.get(x_prev))):
            c[x_prev] = list(nodes.get(x_prev))
        if (x and nodes.get(x) and not isSubsumed(c, nodes.get(x))):
            c[x] = nodes.get(x)


def charm(ip, minSup):
    #print(ip)
    new_ip = ip.copy()
    for i in ip.keys():
        if len(ip.get(i)) < minSup:
            new_ip.pop(i)
    c = {}
    charmExtended(new_ip, c, minSup)

    return c


ip = {'A': [1, 3, 4, 5], 'B': [7, 8, 9, 11], 'C': [1, 2, 3, 4, 5, 6], 'D': [2, 4, 5, 6],
       'T': [1, 3, 5, 6], 'W': [1, 2, 3, 4, 5]}

concepts = charm(ip, 2)
with open('concepts.txt', 'w') as f:
    for z in concepts:
        f.write(z + '\t' +str(concepts[z]) + '\n')